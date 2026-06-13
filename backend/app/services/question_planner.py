from __future__ import annotations

import re
from copy import deepcopy
from typing import Any
from uuid import uuid4

from app.data.catalog import FIELD_VALUE_MAP, MAX_TOTAL_QUESTIONS, QUESTION_BANK, unknown_option
from app.services.document_service import DocumentService, document_service
from app.services.graph_rag_service import GraphRagService, graph_rag_service
from app.services.inquiry_service import InquiryService, inquiry_service
from app.services.slot_utils import (
    admin_term_for,
    append_condition,
    append_unique,
    now_iso,
    set_slot,
    slot_value,
)


class QuestionPlanner:
    def __init__(
        self,
        documents: DocumentService = document_service,
        inquiries: InquiryService = inquiry_service,
        graph_rag: GraphRagService = graph_rag_service,
    ) -> None:
        self.documents = documents
        self.inquiries = inquiries
        self.graph_rag = graph_rag

    def build_question_plan(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        graph_rag_questions = self.graph_rag.build_question_plan(case)
        if graph_rag_questions:
            return self.filter_question_plan(case, graph_rag_questions)

        case.setdefault("ai", {})["questionSource"] = "catalog"
        return self.filter_question_plan(case, QUESTION_BANK)

    @staticmethod
    def filter_question_plan(case: dict[str, Any], questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pending = []
        for question in questions:
            field = question["field"]
            if field == "exact_address" and slot_value(case, "exact_address"):
                continue
            if field == "condition_screening" and "condition_screening" in case["slots"]:
                continue
            if field in case["slots"]:
                continue
            normalized = deepcopy(question)
            if normalized.get("inputMode") in {"single_select", "multi_select"}:
                options = normalized.setdefault("options", [])
                if not any(option.get("id") == "unknown" for option in options):
                    options.append(unknown_option())
            pending.append(normalized)
        return pending[:MAX_TOTAL_QUESTIONS]

    def start_or_finish_question_loop(self, case: dict[str, Any]) -> dict[str, Any]:
        loop = case["questionLoop"]
        next_question = self.next_loop_question(loop)
        if next_question:
            loop["status"] = "active"
            loop["current"] = next_question
            self.record_question_ask(loop, next_question["field"])
            case["machineState"] = "NEEDS_INFO"
            return case

        self.finish_question_loop(case, "completed_or_limited")
        return case

    def next_loop_question(self, loop: dict[str, Any]) -> dict[str, Any] | None:
        if loop["totalAsked"] >= loop["maxTotalQuestions"]:
            loop["stopReason"] = "max_total_questions"
            return None

        answered = set(loop["answeredFields"])
        unknown = set(loop["unknownFields"])
        skipped = set(loop["skippedFields"])
        attempts = loop["attempts"]

        for question in loop["pendingQuestions"]:
            field = question["field"]
            if field in answered or field in unknown or field in skipped:
                continue
            if attempts.get(field, 0) >= loop["maxAttemptsPerField"]:
                append_unique(loop["unknownFields"], field)
                continue
            return question
        return None

    @staticmethod
    def record_question_ask(loop: dict[str, Any], field: str) -> None:
        loop["attempts"][field] = loop["attempts"].get(field, 0) + 1
        append_unique(loop["askedFields"], field)
        loop["totalAsked"] += 1

    def finish_question_loop(self, case: dict[str, Any], reason: str) -> None:
        case["questionLoop"]["status"] = "complete"
        case["questionLoop"]["current"] = None
        case["questionLoop"]["stopReason"] = reason
        case["machineState"] = "DIAGNOSIS"
        # 최초 진단 때만 생성한다. 후속 질문으로 재진입할 때 다시 만들면 이미 완료/해결한
        # 서류·문의 진행 상태가 초기화되어 완료(SUBMITTED) 화면에 영영 도달하지 못한다.
        if not case.get("documents"):
            case["documents"] = self.documents.build_documents(case)
        if not case.get("inquiryTasks"):
            case["inquiryTasks"] = self.inquiries.build_inquiry_tasks(case)

    def followup_fields(self, case: dict[str, Any], fields: list[str]) -> list[str]:
        """후속 질문으로 실제로 물을 수 있는 슬롯 필드만 남긴다.

        LLM 상담 분석이 슬롯키가 아닌 서술형 문장(예: '간판 허가·신고 필요 여부')을
        반환하는 경우를 걸러내, 의미 없는 후속 질문과 무한 루프를 막는다.
        """
        known = {item["field"] for item in QUESTION_BANK}
        answered = set(case["questionLoop"]["answeredFields"])
        return [field for field in fields if field in known and field not in answered]

    def apply_slot_answer(self, case: dict[str, Any], input_payload: dict[str, Any]) -> None:
        loop = case["questionLoop"]
        current = loop.get("current") or {}
        field = input_payload.get("fieldKey") or current.get("field")
        if not field:
            return

        answer_text, value, is_unknown, is_invalid = self.parse_answer(field, input_payload, current)
        question_text = current.get("question") or field

        if is_invalid and loop["attempts"].get(field, 0) < loop["maxAttemptsPerField"]:
            current["validationMessage"] = "답변을 확인하기 어려워요. 아는 만큼만 적거나 ‘아직 몰라요’를 눌러주세요."
            loop["current"] = current
            loop["retryCurrent"] = True
            self.record_question_ask(loop, field)
            return

        if is_unknown or is_invalid:
            append_unique(loop["unknownFields"], field)
            loop["answers"][field] = "unknown"
            set_slot(case, field, "unknown", "미정", admin_term_for(field, "unknown"), status="unknown")
        else:
            append_unique(loop["answeredFields"], field)
            loop["answers"][field] = value
            set_slot(case, field, value, answer_text, admin_term_for(field, value))
            if field == "condition_screening" and isinstance(value, list):
                for item in value:
                    append_condition(case, item)

        case["answers"].append({
            "id": f"answer_{uuid4().hex[:10]}",
            "field": field,
            "question": question_text,
            "answer": answer_text,
            "createdAt": now_iso(),
        })

    def parse_answer(self, field: str, payload: dict[str, Any], current: dict[str, Any]) -> tuple[str, Any, bool, bool]:
        option_ids = payload.get("optionIds") or []
        text = (payload.get("text") or payload.get("value") or "").strip()
        is_unknown = bool(payload.get("unknown")) or "unknown" in option_ids or self.is_unknown_text(text)

        if is_unknown:
            return "미정", "unknown", True, False

        if current.get("inputMode") == "free_text":
            if not text:
                return "미정", "unknown", True, False
            if not self.is_meaningful_text(text):
                return text, text, False, True
            return text, self.normalize_free_text_value(field, text), False, False

        value_map = FIELD_VALUE_MAP.get(field, {})
        values = [value_map.get(option_id, option_id) for option_id in option_ids if option_id != "unknown"]
        if not values:
            return "미정", "unknown", True, False

        labels = {
            option["id"]: option["title"]
            for option in current.get("options", [])
        }
        answer_text = " + ".join(labels.get(option_id, option_id) for option_id in option_ids if option_id != "unknown")
        return answer_text, values if len(values) > 1 else values[0], False, False

    @staticmethod
    def normalize_free_text_value(field: str, text: str) -> Any:
        if field == "exact_address" and re.search(r"미정|모름|몰라|아직", text):
            return "unknown"
        return text

    @staticmethod
    def is_unknown_text(text: str) -> bool:
        compact = re.sub(r"\s+", "", text)
        return compact in {"미정", "모름", "몰라요", "아직몰라요", "아직몰라", "정하지않았어요"}

    @staticmethod
    def is_meaningful_text(text: str) -> bool:
        compact = re.sub(r"\s+", "", text)
        if len(compact) < 2:
            return False
        if compact.lower() in {"asdf", "qwer", "test", "테스트"}:
            return False
        return bool(re.search(r"[가-힣0-9]", text))

    def add_followup_questions(self, case: dict[str, Any], fields: list[str]) -> None:
        loop = case["questionLoop"]
        loop["status"] = "idle"
        loop["current"] = None
        for field in fields:
            if field in loop["answeredFields"]:
                continue
            source = next((item for item in QUESTION_BANK if item["field"] == field), None)
            if not source:
                source = {
                    "field": field,
                    "label": field,
                    "question": f"{field} 정보를 알려주세요.",
                    "why": "새로 확인이 필요해요.",
                    "inputMode": "free_text",
                    "required": True,
                }
            if not any(item["field"] == field for item in loop["pendingQuestions"]):
                loop["pendingQuestions"].append(deepcopy(source))
            if field in loop["unknownFields"]:
                loop["unknownFields"].remove(field)


question_planner = QuestionPlanner()
