from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


BASE_DOCUMENT_KEYS = {
    "building_register",
    "food_business_report_form",
    "hygiene_training_certificate",
    "health_exam_result",
    "lease_contract",
    "id_card",
    "food_business_report_certificate",
    "business_registration_application",
    "business_registration_certificate",
}

CONDITION_DOCUMENT_KEYS = {
    "fire": {"fire_safety_completion_certificate"},
    "lpg": {"lpg_completion_certificate"},
    "signage": {"outdoor_ad_application", "outdoor_ad_design_photo", "outdoor_ad_owner_consent"},
    "outdoor": {"road_occupation_application", "road_location_plan", "road_excavation_drawings"},
    "online": {"ecommerce_purchase_safety"},
}

PREPARE_BEFORE_INQUIRY = {
    "building_register",
    "hygiene_training_certificate",
    "health_exam_result",
    "lease_contract",
    "id_card",
}

BLOCKED_UNTIL_PREVIOUS = {
    "food_business_report_certificate",
    "business_registration_application",
    "business_registration_certificate",
}

DISTRICT_CODES = {
    "종로구": "11110",
    "중구": "11140",
    "용산구": "11170",
    "성동구": "11200",
    "광진구": "11215",
    "동대문구": "11230",
    "중랑구": "11260",
    "성북구": "11290",
    "강북구": "11305",
    "도봉구": "11320",
    "노원구": "11350",
    "은평구": "11380",
    "서대문구": "11410",
    "마포구": "11440",
    "양천구": "11470",
    "강서구": "11500",
    "구로구": "11530",
    "금천구": "11545",
    "영등포구": "11560",
    "동작구": "11590",
    "관악구": "11620",
    "서초구": "11650",
    "강남구": "11680",
    "송파구": "11710",
    "강동구": "11740",
}


class LocalGraphRagRetriever:
    """Use the checked-in minju data package as the primary local GraphRAG source."""

    def __init__(self, root: Path | None = None) -> None:
        repo_root = root or Path(__file__).resolve().parents[3]
        self.minju_root = repo_root / "minju"
        self.graph_root = self.minju_root / "graph"
        self.final_graph_root = self.graph_root / "output" / "final_graph"
        self.nodes_path = self.final_graph_root / "graph_nodes_high_precision.csv"
        self.edges_path = self.final_graph_root / "graph_edges_high_precision.csv"
        self.evidence_path = self.graph_root / "input" / "evidence" / "evidence_chunks_augmented.jsonl"
        self.document_root = self.minju_root / "document_issue_guide"
        self.department_root = self.minju_root / "department_mapping"
        self.form_root = self.minju_root / "form_templates"
        self._core_documents: list[dict[str, str]] | None = None
        self._all_documents: list[dict[str, str]] | None = None
        self._food_documents: list[dict[str, str]] | None = None
        self._prerequisites: list[dict[str, str]] | None = None
        self._department_tasks: list[dict[str, str]] | None = None
        self._department_mappings: list[dict[str, str]] | None = None
        self._form_catalog: dict[str, Any] | None = None
        self._edges: list[dict[str, str]] | None = None
        self._evidence_chunks: list[dict[str, Any]] | None = None

    @property
    def available(self) -> bool:
        return (
            (self.document_root / "document_issue_guide.csv").exists()
            and (self.department_root / "seoul_department_mapping.csv").exists()
        )

    def retrieve(self, kind: str, case: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any] | None:
        if not self.available:
            return None
        if kind == "documents":
            documents = self.build_documents(case)
            return {"documents": documents, "source": "minju"} if documents else None
        if kind == "inquiries":
            tasks = self.build_inquiry_tasks(case)
            return {"inquiryTasks": tasks, "source": "minju"} if tasks else None
        if kind == "questions":
            questions = self.build_question_plan(case)
            return {"questions": questions, "source": "minju"} if questions else None
        if kind == "evidence":
            topic = str((extra or {}).get("topic") or "")
            evidence = self.search_evidence(case, topic)
            return {"evidence": evidence, "source": "minju"} if evidence else None
        return None

    def build_documents(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        selected_keys = self._selected_document_keys(case)
        rows = [row for row in self.core_documents if row.get("document_key") in selected_keys]
        documents = []
        for priority, row in enumerate(rows, start=1):
            key = row["document_key"]
            prerequisites = self._prerequisites_for(row["document_name"])
            form_info = self._form_info(row["document_name"])
            documents.append({
                "id": self._slug(key or row["document_name"]),
                "title": row["document_name"],
                "priority": priority,
                "reason": row.get("required_for") or "민주 데이터 기준으로 준비가 필요한 서류입니다.",
                "status": "blocked" if key in BLOCKED_UNTIL_PREVIOUS else "needs_check",
                "statutoryDeadline": row.get("when_needed") or "확인 필요",
                "perceivedDuration": self._duration_for(row),
                "prerequisites": row.get("prerequisite_summary") or "준비 조건 확인 필요",
                "unlocks": row.get("submit_to") or row.get("required_for") or "다음 인허가 단계",
                "officialLinks": self._official_links(row),
                "prepareInfo": self._prepare_info(row, prerequisites, form_info),
                "steps": self._steps_for(row, prerequisites),
                "canPrepareBeforeInquiry": key in PREPARE_BEFORE_INQUIRY,
                "evidence": self._evidence_for_row(row),
            })
        return documents

    def build_inquiry_tasks(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        documents = self.build_documents(case)
        task_keys = self._ordered_unique(
            self._task_key_for_document_id(document["id"])
            for document in documents
            if self._task_key_for_document_id(document["id"])
        )
        if not task_keys:
            task_keys = ["food_business_report", "building_register_issue"]

        district_code = self._district_code(case)
        tasks = []
        for task_key in task_keys:
            task_meta = self._department_task(task_key)
            mapping = self._department_mapping(task_key, district_code)
            related_docs = [doc for doc in documents if self._task_key_for_document_id(doc["id"]) == task_key]
            title = self._first(mapping, "local_task_label") or self._first(task_meta, "local_task_label") or task_key
            department = self._department_label(mapping)
            tasks.append({
                "id": self._slug(task_key),
                "title": title,
                "department": department,
                "phone": self._phone(self._first(mapping, "phone")),
                "onlineUrl": self._first(mapping, "source_url") or "https://www.epeople.go.kr/index.jsp",
                "visitHint": self._visit_hint(mapping),
                "reason": self._inquiry_reason(title, related_docs, mapping),
                "status": "pending",
                "questions": self._questions_for_task(title, related_docs, mapping),
                "evidence": self._inquiry_evidence(related_docs, mapping),
            })
        return tasks

    def build_question_plan(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        signals = self._signals(case)
        questions: list[dict[str, Any]] = []
        if not self._slot_value(case, "exact_address"):
            questions.append({
                "field": "exact_address",
                "label": "정확한 주소",
                "question": "사업장 주소가 정해졌나요?",
                "why": "민주 부서 매핑 데이터는 자치구 기준으로 실제 담당부서와 연락처를 찾습니다.",
                "inputMode": "free_text",
                "required": True,
            })
        if self._slot_value(case, "on_site_consumption") is None:
            questions.append({
                "field": "on_site_consumption",
                "label": "매장 취식 여부",
                "question": "매장 안에서 손님이 먹고 갈 수 있나요?",
                "why": "소방·식품영업 분기 서류가 달라질 수 있습니다.",
                "inputMode": "single_select",
                "required": True,
                "options": [
                    {"id": "yes", "title": "네, 매장 이용 가능"},
                    {"id": "no", "title": "아니요, 포장이나 배달 중심"},
                ],
            })
        if self._slot_value(case, "liquor_sales") is None:
            questions.append({
                "field": "liquor_sales",
                "label": "주류 판매 여부",
                "question": "주류도 판매할 계획인가요?",
                "why": "업종 확인과 담당부서 문의 문안에 반영됩니다.",
                "inputMode": "single_select",
                "required": True,
                "options": [
                    {"id": "yes", "title": "네, 판매해요"},
                    {"id": "no", "title": "아니요"},
                ],
            })
        if "condition_screening" not in (case.get("slots") or {}):
            options = [
                {"id": "signage_planned", "title": "간판/옥외광고물 설치"},
                {"id": "outdoor_space_planned", "title": "외부 테이블/보도 사용"},
                {"id": "lpg_use", "title": "LPG 또는 가스 사용"},
                {"id": "online_sales_planned", "title": "온라인 주문/배달 판매"},
                {"id": "none", "title": "해당 없음", "exclusive": True},
            ]
            questions.append({
                "field": "condition_screening",
                "label": "추가 조건",
                "question": "민주 데이터 기준으로 추가 확인할 조건이 있나요?",
                "why": "간판, 도로점용, LPG, 통신판매 서류를 자동으로 추가합니다.",
                "inputMode": "multi_select",
                "required": False,
                "options": options,
            })
        if signals.get("outdoor") and not self._slot_value(case, "building_use"):
            questions.append({
                "field": "building_use",
                "label": "건축물 용도",
                "question": "건축물대장상 용도를 알고 있나요?",
                "why": "도로점용·영업신고 전 용도 적합성 확인이 필요합니다.",
                "inputMode": "free_text",
                "required": False,
            })
        return questions

    def search_evidence(self, case: dict[str, Any], topic: str) -> list[dict[str, str]]:
        tokens = self._tokens(
            " ".join([
                topic,
                str(case.get("rawInput") or ""),
                " ".join(str(slot.get("value") or "") for slot in (case.get("slots") or {}).values() if isinstance(slot, dict)),
            ])
        )
        if not tokens:
            tokens = {"식품", "영업", "신고"}

        candidates: list[tuple[int, dict[str, str]]] = []
        for row in [*self.core_documents, *self.food_documents, *self.all_documents]:
            text = " ".join(str(row.get(key) or "") for key in ("document_name", "required_for", "when_needed", "evidence_text", "source_title"))
            score = self._score(tokens, text)
            if score:
                candidates.append((score + 2, {
                    "title": row.get("source_title") or row.get("document_name") or "민주 근거",
                    "url": self._safe_url(row.get("source_url", "")),
                    "excerpt": self._shorten(row.get("evidence_text") or row.get("prerequisite_summary") or ""),
                }))
        for edge in self.edges:
            text = " ".join(str(edge.get(key) or "") for key in ("subject_name", "object_name", "condition_text", "evidence_text", "title"))
            score = self._score(tokens, text)
            if score:
                candidates.append((score, {
                    "title": edge.get("source_title") or edge.get("subject_name") or "민주 그래프 근거",
                    "url": self._safe_url(edge.get("source_url", "")),
                    "excerpt": self._shorten(edge.get("evidence_text") or edge.get("condition_text") or ""),
                }))
        return self._top_unique_evidence(candidates)

    @property
    def core_documents(self) -> list[dict[str, str]]:
        if self._core_documents is None:
            self._core_documents = self._read_csv(self.document_root / "document_issue_guide.csv")
        return self._core_documents

    @property
    def all_documents(self) -> list[dict[str, str]]:
        if self._all_documents is None:
            self._all_documents = self._read_csv(self.document_root / "all_document_issue_guide.csv")
        return self._all_documents

    @property
    def food_documents(self) -> list[dict[str, str]]:
        if self._food_documents is None:
            self._food_documents = self._read_csv(self.document_root / "food_permit_submission_documents.csv")
        return self._food_documents

    @property
    def prerequisites(self) -> list[dict[str, str]]:
        if self._prerequisites is None:
            self._prerequisites = self._read_csv(self.document_root / "document_prerequisites.csv")
        return self._prerequisites

    @property
    def department_tasks(self) -> list[dict[str, str]]:
        if self._department_tasks is None:
            self._department_tasks = self._read_csv(self.department_root / "local_department_tasks.csv")
        return self._department_tasks

    @property
    def department_mappings(self) -> list[dict[str, str]]:
        if self._department_mappings is None:
            self._department_mappings = self._read_csv(self.department_root / "seoul_department_mapping.csv")
        return self._department_mappings

    @property
    def form_catalog(self) -> dict[str, Any]:
        if self._form_catalog is None:
            path = self.form_root / "form_template_catalog.json"
            self._form_catalog = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return self._form_catalog

    @property
    def edges(self) -> list[dict[str, str]]:
        if self._edges is None:
            self._edges = self._read_csv(self.edges_path)
        return self._edges

    def _selected_document_keys(self, case: dict[str, Any]) -> set[str]:
        signals = self._signals(case)
        keys = set(BASE_DOCUMENT_KEYS)
        for condition, document_keys in CONDITION_DOCUMENT_KEYS.items():
            if signals.get(condition):
                keys.update(document_keys)
        return keys

    def _signals(self, case: dict[str, Any]) -> dict[str, bool]:
        raw = str(case.get("rawInput") or "")
        conditions = self._slot_value(case, "condition_screening")
        if not isinstance(conditions, list):
            conditions = [conditions] if conditions else []
        condition_set = {str(item) for item in conditions}
        return {
            "fire": self._slot_value(case, "on_site_consumption") is True or "lpg_use" in condition_set or bool(re.search("객석|좌석|매장|지하|LPG|가스", raw, re.I)),
            "lpg": "lpg_use" in condition_set or bool(re.search("LPG|가스", raw, re.I)),
            "signage": "signage_planned" in condition_set or bool(re.search("간판|옥외광고", raw)),
            "outdoor": "outdoor_space_planned" in condition_set or bool(re.search("테라스|야외|외부|보도|도로점용", raw)),
            "online": "online_sales_planned" in condition_set or bool(re.search("온라인|배달|택배|통신판매", raw)),
        }

    def _district_code(self, case: dict[str, Any]) -> str:
        text = " ".join([
            str(case.get("rawInput") or ""),
            str(self._slot_value(case, "exact_address") or ""),
        ])
        for district, code in DISTRICT_CODES.items():
            if district in text:
                return code
        return "11440"

    def _department_task(self, task_key: str) -> dict[str, str]:
        return next((row for row in self.department_tasks if row.get("local_task_key") == task_key), {})

    def _department_mapping(self, task_key: str, district_code: str) -> dict[str, str]:
        exact = [
            row for row in self.department_mappings
            if row.get("district_code") == district_code and row.get("local_task_key") == task_key
        ]
        if exact:
            return exact[0]
        fallback = [row for row in self.department_mappings if row.get("local_task_key") == task_key]
        return fallback[0] if fallback else {}

    def _task_key_for_document_id(self, document_id: str) -> str:
        key = document_id.replace("-", "_")
        row = next((item for item in self.core_documents if item.get("document_key") == key), None)
        return (row or {}).get("submit_to_local_task_key", "")

    def _prerequisites_for(self, document_name: str) -> list[str]:
        values = [
            row["prerequisite_name"]
            for row in self.prerequisites
            if row.get("target_document_or_step") == document_name and row.get("prerequisite_name")
        ]
        return self._ordered_unique(values)

    def _form_info(self, document_name: str) -> dict[str, Any]:
        documents = self.form_catalog.get("documents", [])
        if not isinstance(documents, list):
            return {}
        normalized = self._normalize(document_name)
        return next((item for item in documents if self._normalize(str(item.get("document_name") or "")) == normalized), {})

    def _duration_for(self, row: dict[str, str]) -> str:
        text = " ".join([row.get("when_needed", ""), row.get("issue_channel", "")])
        if "즉시" in text or "온라인" in text:
            return "즉시 또는 당일"
        if "검사" in row.get("document_name", "") or "건강" in row.get("document_name", ""):
            return "약 4~5일"
        if "소방" in row.get("document_group", ""):
            return "현장 확인 필요"
        return "발급/준비처 확인"

    def _prepare_info(self, row: dict[str, str], prerequisites: list[str], form_info: dict[str, Any]) -> list[str]:
        values = [
            row.get("issue_or_prepare_place", ""),
            row.get("issue_channel", ""),
            row.get("prerequisite_summary", ""),
            *prerequisites,
        ]
        required_inputs = form_info.get("required_inputs")
        if isinstance(required_inputs, list):
            values.extend(str(item) for item in required_inputs[:4])
        return self._ordered_unique(self._clean_parts(values))[:6] or ["준비 정보 확인 필요"]

    def _steps_for(self, row: dict[str, str], prerequisites: list[str]) -> list[str]:
        steps = [
            row.get("prerequisite_summary", ""),
            f"{row.get('issue_or_prepare_place', '발급/준비처')}에서 {row.get('document_name', '서류')} 준비",
            row.get("submit_to", ""),
        ]
        steps.extend(prerequisites[:2])
        return self._ordered_unique(self._clean_parts(steps))[:4]

    def _official_links(self, row: dict[str, str]) -> list[dict[str, str]]:
        url = self._safe_url(row.get("source_url", ""))
        if not url:
            return [{"label": "정부24에서 확인", "url": "https://www.gov.kr"}]
        return [{"label": row.get("source_title") or "공식 근거", "url": url}]

    def _evidence_for_row(self, row: dict[str, str]) -> list[str]:
        return self._clean_parts([
            self._shorten(row.get("evidence_text", ""), 180),
            row.get("section_path", ""),
        ])[:2]

    def _department_label(self, mapping: dict[str, str]) -> str:
        department = self._first(mapping, "actual_department_name") or "담당부서 확인 필요"
        team = self._first(mapping, "actual_team_name")
        district = self._first(mapping, "district_name")
        return " ".join(item for item in [district, department, team] if item)

    def _visit_hint(self, mapping: dict[str, str]) -> str:
        office = self._first(mapping, "office_name") or "관할 구청"
        address = self._first(mapping, "office_address")
        return f"{office} ({address})" if address else office

    def _inquiry_reason(self, title: str, docs: list[dict[str, Any]], mapping: dict[str, str]) -> str:
        names = ", ".join(doc["title"] for doc in docs[:3])
        evidence = self._first(mapping, "evidence_text")
        if names:
            return f"{title} 단계에서 {names} 제출/확인 기준을 담당부서에 확인해야 합니다."
        return self._shorten(evidence, 160) or f"{title} 담당부서 확인이 필요합니다."

    def _questions_for_task(self, title: str, docs: list[dict[str, Any]], mapping: dict[str, str]) -> list[str]:
        questions = [
            f"{title} 처리 기준과 접수 채널은 무엇인가요?",
            "현재 주소와 업종 기준으로 추가 확인할 조건이 있나요?",
        ]
        for doc in docs[:3]:
            questions.append(f"{doc['title']}은 어떤 형식으로 준비하거나 제출하면 되나요?")
        if mapping.get("actual_team_name"):
            questions.append(f"{mapping['actual_team_name']}에서 바로 확인 가능한 업무인가요?")
        return self._ordered_unique(questions)[:5]

    def _inquiry_evidence(self, docs: list[dict[str, Any]], mapping: dict[str, str]) -> list[str]:
        evidence = [self._first(mapping, "evidence_text")]
        for doc in docs:
            evidence.extend(doc.get("evidence", []))
        return self._ordered_unique(self._clean_parts(evidence))[:3]

    @staticmethod
    def _slot_value(case: dict[str, Any], field: str) -> Any:
        slot = (case.get("slots") or {}).get(field)
        return slot.get("value") if isinstance(slot, dict) else None

    @staticmethod
    def _read_csv(path: Path) -> list[dict[str, str]]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            return [dict(row) for row in csv.DictReader(file)]

    @staticmethod
    def _first(mapping: dict[str, str], key: str) -> str:
        return str(mapping.get(key) or "").strip()

    @staticmethod
    def _phone(value: str) -> str:
        digits = re.sub(r"[^0-9+]", "", value or "")
        return f"tel:{digits}" if digits else "tel:120"

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {token.lower() for token in re.findall(r"[가-힣A-Za-z0-9]{2,}", text or "")}

    @staticmethod
    def _score(tokens: set[str], text: str) -> int:
        lower_text = (text or "").lower()
        return sum(1 for token in tokens if token in lower_text)

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\s+|/|ㆍ|·", "", value or "")

    @staticmethod
    def _slug(value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", value or "").strip("-").lower()
        return slug or "minju-item"

    @staticmethod
    def _safe_url(url: str) -> str:
        url = (url or "").strip()
        if not url.startswith(("http://", "https://")) or "REDACTED" in url:
            return ""
        return url

    @staticmethod
    def _shorten(text: str, max_length: int = 220) -> str:
        compact = re.sub(r"\s+", " ", text or "").strip()
        if len(compact) <= max_length:
            return compact
        return compact[: max_length - 1].rstrip() + "…"

    @staticmethod
    def _clean_parts(values: list[str]) -> list[str]:
        return [str(value).strip() for value in values if str(value).strip()]

    @staticmethod
    def _ordered_unique(values: Any) -> list[str]:
        items: list[str] = []
        for value in values:
            text = str(value or "").strip()
            if text and text not in items:
                items.append(text)
        return items

    def _top_unique_evidence(self, candidates: list[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
        results = []
        seen = set()
        for _, item in sorted(candidates, key=lambda candidate: candidate[0], reverse=True):
            key = (item["title"], item["excerpt"])
            if key in seen or not item["excerpt"]:
                continue
            seen.add(key)
            results.append(item)
            if len(results) >= 5:
                break
        return results


local_graph_rag = LocalGraphRagRetriever()
