from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.data.catalog import MAX_ATTEMPTS_PER_FIELD, MAX_TOTAL_QUESTIONS
from app.services.slot_utils import now_iso


def new_case(raw_text: str) -> dict[str, Any]:
    return {
        "caseId": f"case_{uuid4().hex[:12]}",
        "machineState": "UNDERSTAND",
        "rawInput": raw_text.strip(),
        "slots": {},
        "candidatePermits": [],
        "answers": [],
        "documents": [],
        "inquiryTasks": [],
        "completedDocumentIds": [],
        "selectedInquiryChannel": "channels",
        "ai": {
            "intakeSource": "rules",
            "consultationSource": "rules",
            "warnings": [],
        },
        "questionLoop": {
            "status": "idle",
            "maxTotalQuestions": MAX_TOTAL_QUESTIONS,
            "maxAttemptsPerField": MAX_ATTEMPTS_PER_FIELD,
            "askedFields": [],
            "answeredFields": [],
            "unknownFields": [],
            "skippedFields": [],
            "answers": {},
            "attempts": {},
            "pendingQuestions": [],
            "current": None,
            "totalAsked": 0,
            "stopReason": "",
        },
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
