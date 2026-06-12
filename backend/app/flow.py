from __future__ import annotations

from typing import Any

from app.services.flow_service import flow_service


# Backward-compatible facade for the existing FastAPI endpoints.
# New backend logic lives in app.services.* and app.repositories.*.
CASES = flow_service.cases


def create_case(raw_text: str) -> dict[str, Any]:
    return flow_service.create_case(raw_text)


def apply_turn(case_id: str, input_payload: dict[str, Any]) -> dict[str, Any]:
    return flow_service.apply_turn(case_id, input_payload)


def envelope(case: dict[str, Any]) -> dict[str, Any]:
    return flow_service.envelope(case)
