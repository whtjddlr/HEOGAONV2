from __future__ import annotations

import re
from typing import Any

from pydantic import ValidationError

from app.integrations.llm_client import LlmClient, llm_client
from app.schemas.ai import IntakeResult
from app.services.output_guard import mask_sensitive_text
from app.services.slot_utils import append_condition, set_slot, slot_value


class IntakeAgent:
    def __init__(self, llm: LlmClient = llm_client) -> None:
        self.llm = llm

    def understand(self, case: dict[str, Any]) -> None:
        text = mask_sensitive_text(case["rawInput"])
        ai_result = self._ai_intake(text)
        if ai_result:
            self._apply_ai_result(case, ai_result)
            case["ai"]["intakeSource"] = "llm"

        self._apply_rule_fallback(case, text)
        case["candidatePermits"] = self.infer_candidate_permits(case)

    def _ai_intake(self, text: str) -> IntakeResult | None:
        result = self.llm.generate_json(
            system_prompt=(
                "너는 요식업 인허가 준비 입력을 구조화하는 IntakeAgent다. "
                "허가 가능 여부를 판단하지 말고 명시된 사실만 추출한다. "
                "모르는 값은 비워두거나 unknowns에 넣는다. JSON만 반환한다."
            ),
            user_payload={
                "rawText": text,
                "schema": {
                    "intent": "food|signage|outdoor|general|unsupported",
                    "business_type": "string|null",
                    "region": "string|null",
                    "address": "string|null",
                    "building_use": "string|null",
                    "sales_modes": "string[]",
                    "signage_wanted": "boolean",
                    "outdoor_wanted": "boolean",
                    "liquor_sales": "boolean|null",
                    "on_site_consumption": "boolean|null",
                    "manufacturing_mode": "cook|manufacturing_or_processing|resale_or_simple_sale|null",
                    "unknowns": "string[]",
                    "confidence": "number",
                },
            },
        )
        if not result:
            return None
        try:
            return IntakeResult.model_validate(result)
        except ValidationError:
            return None

    def _apply_ai_result(self, case: dict[str, Any], result: IntakeResult) -> None:
        if result.region and "location" not in case["slots"]:
            set_slot(case, "location", result.region, result.region, "AI 추출 지역")
        if result.business_type and "business_activity" not in case["slots"]:
            set_slot(case, "business_activity", result.business_type, result.business_type, "AI 추출 업종")
        if result.address and "exact_address" not in case["slots"]:
            set_slot(case, "exact_address", result.address, result.address, "AI 추출 주소")
        if result.building_use and "building_use" not in case["slots"]:
            set_slot(case, "building_use", result.building_use, result.building_use, "AI 추출 건축물 용도")
        if result.on_site_consumption is not None and "on_site_consumption" not in case["slots"]:
            text = "매장 안에서 먹고 갈 수 있어요" if result.on_site_consumption else "포장·배달만 해요"
            admin = "객석 있음 / 식품접객업 검토" if result.on_site_consumption else "객석 없음 / 포장·배달 검토"
            set_slot(case, "on_site_consumption", result.on_site_consumption, text, admin)
        if result.liquor_sales is not None and "liquor_sales" not in case["slots"]:
            text = "술 판매 가능성이 있어요" if result.liquor_sales else "술 판매 없음"
            set_slot(case, "liquor_sales", result.liquor_sales, text, "AI 추출 주류 판매 여부")
        if result.manufacturing_mode and "manufacturing_or_simple_sale" not in case["slots"]:
            set_slot(case, "manufacturing_or_simple_sale", result.manufacturing_mode, result.manufacturing_mode, "AI 추출 조리·제조 방식")
        if result.signage_wanted:
            append_condition(case, "signage_planned")
        if result.outdoor_wanted:
            append_condition(case, "outdoor_space_planned")

    def _apply_rule_fallback(self, case: dict[str, Any], text: str) -> None:
        location = self.infer_location(text)
        if location and "location" not in case["slots"]:
            set_slot(case, "location", location, location, "사용자 입력 지역")

        activity = self.infer_business_activity(text)
        if activity and "business_activity" not in case["slots"]:
            set_slot(case, "business_activity", activity, activity, "생활 언어 업종")

        if re.search(r"매장|홀|좌석|먹고|취식", text) and "on_site_consumption" not in case["slots"]:
            set_slot(case, "on_site_consumption", True, "매장 안에서 먹고 갈 수 있어요", "객석 있음 / 식품접객업 검토")
        if re.search(r"포장|배달", text) and "operation_detail" not in case["slots"]:
            set_slot(case, "operation_detail", ["takeout", "delivery"], "포장·배달도 해요", "포장·배달 판매")
        if re.search(r"술|주류|맥주|와인|소주", text) and "liquor_sales" not in case["slots"]:
            set_slot(case, "liquor_sales", True, "술 판매 가능성이 있어요", "주류 판매 검토")
        if re.search(r"간판|옥외광고", text):
            append_condition(case, "signage_planned")
        if re.search(r"외부|테이블|보도|도로", text):
            append_condition(case, "outdoor_space_planned")

    @staticmethod
    def infer_location(text: str) -> str | None:
        for pattern in [r"([가-힣]+동)", r"([가-힣]+구)", r"(홍대|합정|연남|망원)"]:
            match = re.search(pattern, text)
            if match:
                value = match.group(1)
                return {"연남": "연남동", "망원": "망원동"}.get(value, value)
        return None

    @staticmethod
    def infer_business_activity(text: str) -> str | None:
        if re.search(r"디저트|카페|커피|음료", text):
            return "디저트 카페"
        if re.search(r"고깃|고기|삼겹|갈비", text):
            return "고깃집"
        if re.search(r"음식점|식당|요식", text):
            return "음식점"
        return None

    @staticmethod
    def infer_candidate_permits(case: dict[str, Any]) -> list[dict[str, str]]:
        activity = slot_value(case, "business_activity") or ""
        candidates: list[dict[str, str]] = []
        if "카페" in activity or "디저트" in activity:
            candidates.extend([
                candidate("휴게음식점영업", "음료·디저트 판매 가능성"),
                candidate("제과점영업", "직접 빵·과자류 제조 가능성"),
                candidate("즉석판매제조·가공업", "제조 후 포장 판매 가능성"),
            ])
        elif "고깃" in activity or "음식" in activity:
            candidates.append(candidate("일반음식점영업", "조리 음식과 객석 운영 가능성"))
        else:
            candidates.append(candidate("식품관련 영업신고", "요식업 준비 입력"))
        return candidates


def candidate(name: str, reason: str) -> dict[str, str]:
    return {"name": name, "status": "candidate", "reason": reason}


intake_agent = IntakeAgent()
