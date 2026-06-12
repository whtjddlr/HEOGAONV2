from __future__ import annotations

from typing import Any

from app.models.case_factory import new_case
from app.repositories.case_repository import InMemoryCaseRepository, case_repository
from app.services.consultation_analyzer import ConsultationAnalyzer, consultation_analyzer
from app.services.document_service import DocumentService, document_service
from app.services.inquiry_service import InquiryService, inquiry_service
from app.services.intake_agent import IntakeAgent, intake_agent
from app.services.question_planner import QuestionPlanner, question_planner
from app.services.slot_utils import now_iso
from app.services.view_builder import ViewBuilder, view_builder


class CaseFlowService:
    def __init__(
        self,
        repository: InMemoryCaseRepository = case_repository,
        intake: IntakeAgent = intake_agent,
        questions: QuestionPlanner = question_planner,
        documents: DocumentService = document_service,
        inquiries: InquiryService = inquiry_service,
        consultations: ConsultationAnalyzer = consultation_analyzer,
        views: ViewBuilder = view_builder,
    ) -> None:
        self.repository = repository
        self.intake = intake
        self.questions = questions
        self.documents = documents
        self.inquiries = inquiries
        self.consultations = consultations
        self.views = views

    @property
    def cases(self) -> dict[str, dict[str, Any]]:
        return self.repository.cases

    def create_case(self, raw_text: str) -> dict[str, Any]:
        case = new_case(raw_text)
        self.intake.understand(case)
        case["questionLoop"]["pendingQuestions"] = self.questions.build_question_plan(case)
        self.repository.add(case)
        return self.questions.start_or_finish_question_loop(case)

    def apply_turn(self, case_id: str, input_payload: dict[str, Any]) -> dict[str, Any]:
        case = self.repository.get(case_id)
        if not case:
            text = input_payload.get("text") or ""
            return self.create_case(text)

        input_type = input_payload.get("type")
        case["updatedAt"] = now_iso()

        if input_type == "slot_answer":
            self.questions.apply_slot_answer(case, input_payload)
            if case["questionLoop"].pop("retryCurrent", False):
                return case
            return self.questions.start_or_finish_question_loop(case)

        if input_type == "action":
            return self.apply_action(case, input_payload.get("actionId", "primary"))

        if input_type == "document_toggle":
            self.documents.toggle_document(case, input_payload.get("documentId"), bool(input_payload.get("completed")))
            case["machineState"] = "DOCUMENTS"
            return case

        if input_type == "inquiry_channel":
            case["machineState"] = "INQUIRY"
            case["selectedInquiryChannel"] = input_payload.get("channel") or "channels"
            return case

        if input_type == "consultation_answer":
            self.consultations.analyze(case, input_payload.get("text") or "")
            return case

        return case

    def apply_action(self, case: dict[str, Any], action_id: str) -> dict[str, Any]:
        state = case["machineState"]
        if action_id == "restart":
            return self.create_case("")
        if action_id == "documents":
            case["machineState"] = "DOCUMENTS"
            return case
        if action_id == "inquiry":
            case["machineState"] = "INQUIRY"
            case["selectedInquiryChannel"] = "channels"
            return case
        if action_id == "dashboard":
            case["machineState"] = "DASHBOARD"
            return case
        if action_id == "submitted":
            case["machineState"] = "SUBMITTED" if self.all_documents_completed(case) and not self.inquiries.has_open_inquiry(case) else "DASHBOARD"
            return case

        if state == "DIAGNOSIS":
            case["machineState"] = "DOCUMENTS"
            return case

        if state == "DOCUMENTS":
            if not self.all_documents_completed(case):
                case["machineState"] = "DOCUMENTS"
                return case
            if self.inquiries.has_open_inquiry(case):
                case["machineState"] = "INQUIRY"
                case["selectedInquiryChannel"] = "channels"
            else:
                case["machineState"] = "DASHBOARD"
            return case

        if state == "INQUIRY":
            case["machineState"] = "ANSWER_REVIEW"
            return case

        if state == "ANSWER_REVIEW":
            return self.route_after_answer_review(case)

        if state == "DASHBOARD":
            if self.inquiries.has_open_inquiry(case):
                case["machineState"] = "INQUIRY"
                case["selectedInquiryChannel"] = "channels"
                return case
            if any(document["status"] != "completed" for document in case["documents"]):
                case["machineState"] = "DOCUMENTS"
                return case
            case["machineState"] = "SUBMITTED"
            return case

        if state == "SUBMITTED":
            case["machineState"] = "DASHBOARD"
            return case

        return case

    @staticmethod
    def all_documents_completed(case: dict[str, Any]) -> bool:
        documents = case.get("documents") or []
        completed_ids = set(case.get("completedDocumentIds") or [])
        return all(document["id"] in completed_ids or document.get("status") == "completed" for document in documents)

    def route_after_answer_review(self, case: dict[str, Any]) -> dict[str, Any]:
        analysis = case.get("lastAnswerAnalysis") or {}
        if analysis.get("newMissingFields"):
            self.questions.add_followup_questions(case, analysis["newMissingFields"])
            return self.questions.start_or_finish_question_loop(case)
        if analysis.get("newInquiryTasks"):
            case["machineState"] = "INQUIRY"
            case["selectedInquiryChannel"] = "channels"
            return case
        if analysis.get("nextAction") == "documents":
            case["machineState"] = "DOCUMENTS"
            return case
        case["machineState"] = "DASHBOARD"
        return case

    def envelope(self, case: dict[str, Any]) -> dict[str, Any]:
        return self.views.envelope(case)


flow_service = CaseFlowService()
