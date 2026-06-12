from __future__ import annotations

from typing import Any

from app.data.catalog import DOCUMENT_PRIORITY_RULES
from app.services.slot_utils import as_list, slot_value


class DocumentService:
    def build_documents(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        selected = [
            self.document_from_rule("building-ledger", "needs_check"),
            self.document_from_rule("health-check", "not_started"),
            self.document_from_rule("hygiene-education", "not_started"),
            self.document_from_rule("food-business-report", "needs_check"),
            self.document_from_rule("business-registration", "blocked"),
        ]

        conditions = set(as_list(slot_value(case, "condition_screening")))
        if slot_value(case, "on_site_consumption") is True or "lpg_use" in conditions:
            selected.append(self.document_from_rule("fire-safety", "needs_check"))
        if "lpg_use" in conditions:
            selected.append(self.document_from_rule("lpg-certificate", "needs_check"))
        if "signage_planned" in conditions:
            selected.append(self.document_from_rule("signage-report", "needs_check"))

        return sorted(selected, key=lambda item: item["priority"])

    def toggle_document(self, case: dict[str, Any], document_id: str | None, completed: bool) -> None:
        if not document_id:
            return
        completed_ids = set(case["completedDocumentIds"])
        if completed:
            completed_ids.add(document_id)
        else:
            completed_ids.discard(document_id)
        case["completedDocumentIds"] = sorted(completed_ids)
        for document in case["documents"]:
            if document["id"] == document_id:
                document["status"] = "completed" if completed else "not_started"

    def document_from_rule(self, rule_id: str, status: str) -> dict[str, Any]:
        rule = next(item for item in DOCUMENT_PRIORITY_RULES if item["id"] == rule_id)
        return {
            "id": rule["id"],
            "title": rule["title"],
            "priority": rule["priority"],
            "reason": rule["reason"],
            "status": status,
            "statutoryDeadline": rule["statutoryDeadline"],
            "perceivedDuration": rule["perceivedDuration"],
            "prerequisites": rule["prerequisites"],
            "unlocks": rule["unlocks"],
            "officialLinks": self.official_links_for(rule["id"]),
            "prepareInfo": self.prepare_info_for(rule["id"]),
            "steps": self.steps_for(rule["id"]),
            "canPrepareBeforeInquiry": rule["id"] in {"health-check", "hygiene-education", "building-ledger"},
        }

    @staticmethod
    def official_links_for(rule_id: str) -> list[dict[str, str]]:
        if rule_id == "building-ledger":
            return [{"label": "정부24 건축물대장", "url": "https://www.gov.kr"}]
        if rule_id == "food-business-report":
            return [{"label": "정부24 식품관련영업신고", "url": "https://www.gov.kr"}]
        return [{"label": "정부24에서 확인", "url": "https://www.gov.kr"}]

    @staticmethod
    def prepare_info_for(rule_id: str) -> list[str]:
        mapping = {
            "building-ledger": ["정확한 주소", "층수", "위반건축물 여부"],
            "health-check": ["창업자/종사자 이름", "검진기관", "발급일"],
            "hygiene-education": ["영업자 정보", "후보 업종", "수료기관"],
            "food-business-report": ["후보 영업신고 유형", "선행 서류 완료 여부", "영업장 정보"],
            "business-registration": ["영업신고증", "임대차계약서", "대표자 정보"],
            "fire-safety": ["면적", "층수", "시설 구조", "소방 설비 상태"],
            "lpg-certificate": ["가스 설비 시공 상태", "화구 종류", "검사 일정"],
            "signage-report": ["간판 위치", "크기", "조명 여부", "디자인 도면"],
        }
        return mapping.get(rule_id, ["신청 정보"])

    @staticmethod
    def steps_for(rule_id: str) -> list[str]:
        mapping = {
            "building-ledger": ["주소 확정", "건축물대장 조회", "용도와 위반 여부 확인"],
            "health-check": ["검진기관 확인", "검진 진행", "결과서 발급 후 보관"],
            "hygiene-education": ["교육 대상 확인", "온라인/오프라인 수료", "수료증 저장"],
            "food-business-report": ["선행 서류 확인", "보건소 위생과 문의", "영업신고 접수"],
            "business-registration": ["영업신고증 준비", "세무서/홈택스 신청", "사업자등록증 발급 확인"],
            "fire-safety": ["대상 여부 문의", "현장 실사 일정 조율", "증명서 발급"],
            "lpg-certificate": ["시공 완료", "검사 신청", "필증 발급"],
            "signage-report": ["간판 자료 정리", "옥외광고물 담당 문의", "허가·신고 여부 반영"],
        }
        return mapping.get(rule_id, ["필요 항목 확인", "공식 사이트 확인", "완료 표시"])


document_service = DocumentService()
