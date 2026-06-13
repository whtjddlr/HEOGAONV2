from __future__ import annotations

from typing import Any

from app.integrations.llm_client import LlmClient, llm_client
from app.services.graph_rag_service import GraphRagService, graph_rag_service
from app.services.output_guard import clean_text
from app.services.slot_utils import as_list, slot_value

SEOUL_DISTRICTS = [
    "종로구",
    "중구",
    "용산구",
    "성동구",
    "광진구",
    "동대문구",
    "중랑구",
    "성북구",
    "강북구",
    "도봉구",
    "노원구",
    "은평구",
    "서대문구",
    "마포구",
    "양천구",
    "강서구",
    "구로구",
    "금천구",
    "영등포구",
    "동작구",
    "관악구",
    "서초구",
    "강남구",
    "송파구",
    "강동구",
]

MAPO_AREA_HINTS = {"홍대", "합정", "연남", "연남동", "망원", "망원동"}


class InquiryService:
    def __init__(
        self,
        llm: LlmClient = llm_client,
        graph_rag: GraphRagService = graph_rag_service,
    ) -> None:
        self.llm = llm
        self.graph_rag = graph_rag

    def build_inquiry_tasks(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        graph_rag_tasks = self.graph_rag.build_inquiry_tasks(case)
        if graph_rag_tasks:
            return graph_rag_tasks

        case.setdefault("ai", {})["inquirySource"] = "catalog"
        district = self.district_for_case(case)
        tasks = [
            {
                "id": "food-business-type",
                "title": "영업신고 유형 확인",
                "department": f"{district} 보건소 위생과",
                "phone": "tel:0231539180",
                "onlineUrl": "https://www.epeople.go.kr/index.jsp",
                "visitHint": f"{district} 보건소 또는 구청 위생 민원 창구",
                "reason": "우리 가게에 맞는 신고 유형을 확인해야 해요.",
                "status": "pending",
                "questions": [
                    "제 가게는 어떤 영업신고 유형을 보면 될까요?",
                    "건물 용도나 객석 기준으로 더 필요한 서류가 있나요?",
                    "지금 먼저 준비할 수 있는 서류가 있나요?",
                ],
            }
        ]
        conditions = set(as_list(slot_value(case, "condition_screening")))
        if "signage_planned" in conditions:
            tasks.append({
                "id": "signage-check",
                "title": "간판 신고 확인",
                "department": f"{district} 옥외광고물 담당",
                "phone": "tel:120",
                "onlineUrl": "https://www.epeople.go.kr/index.jsp",
                "visitHint": f"{district} 구청 도시경관 또는 옥외광고물 담당 창구",
                "reason": "간판 위치와 크기 기준을 확인해야 해요.",
                "status": "pending",
                "questions": [
                    "이 간판이 신고 대상인가요?",
                    "도면, 크기, 조명 정보 중 무엇을 준비하면 되나요?",
                ],
            })
        if "outdoor_space_planned" in conditions:
            tasks.append({
                "id": "road-occupation-check",
                "title": "외부 공간 사용 확인",
                "department": f"{district} 도로관리과",
                "phone": "tel:120",
                "onlineUrl": "https://www.epeople.go.kr/index.jsp",
                "visitHint": f"{district} 구청 도로점용 담당 창구",
                "reason": "가게 앞 공간 사용 가능 여부를 확인해야 해요.",
                "status": "pending",
                "questions": [
                    "가게 앞 테이블 설치가 가능한가요?",
                    "사유지와 보도 경계 확인에 필요한 자료가 있나요?",
                ],
            })
        return tasks

    @staticmethod
    def district_for_case(case: dict[str, Any]) -> str:
        text = " ".join(
            str(value or "")
            for value in [
                slot_value(case, "location"),
                slot_value(case, "exact_address"),
                case.get("rawInput", ""),
            ]
        )
        for district in SEOUL_DISTRICTS:
            if district in text:
                return district
        if any(hint in text for hint in MAPO_AREA_HINTS):
            return "마포구"
        return "마포구"

    def online_draft(self, case: dict[str, Any], task: dict[str, Any] | None) -> dict[str, str]:
        if not task:
            return {"subject": "인허가 문의", "body": "확인할 문의가 없습니다."}

        ai_draft = self._ai_online_draft(case, task)
        if ai_draft:
            return ai_draft

        body = [
            "[상황 요약]",
            case["rawInput"] or "요식업 창업을 준비 중입니다.",
            "",
            "[문의할 내용]",
            *[f"{index + 1}. {question}" for index, question in enumerate(task["questions"])],
            "",
            "[담당 부서 후보]",
            task["department"],
        ]
        return {"subject": task["title"], "body": clean_text("\n".join(body))}

    def _ai_online_draft(self, case: dict[str, Any], task: dict[str, Any]) -> dict[str, str] | None:
        result = self.llm.generate_json(
            system_prompt=(
                "너는 인허가 문의 문안을 작성하는 도우미다. "
                "허가 가능 여부를 단정하지 말고, 담당 부서가 확인할 질문만 작성한다. "
                "JSON {\"subject\": string, \"body\": string}만 반환한다."
            ),
            user_payload={
                "rawInput": case.get("rawInput", ""),
                "slots": case.get("slots", {}),
                "task": task,
            },
        )
        if not result or not isinstance(result.get("body"), str):
            return None
        return {
            "subject": clean_text(str(result.get("subject") or task["title"])),
            "body": clean_text(result["body"]),
        }

    @staticmethod
    def has_open_inquiry(case: dict[str, Any]) -> bool:
        return any(task["status"] == "pending" for task in case["inquiryTasks"])


inquiry_service = InquiryService()
