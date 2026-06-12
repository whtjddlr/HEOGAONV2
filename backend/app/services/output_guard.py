from __future__ import annotations

import re
from typing import Any


FORBIDDEN_REPLACEMENTS = {
    "허가됩니다": "담당 부서 확인이 필요합니다",
    "가능합니다": "조건에 따라 달라질 수 있습니다",
    "문제없습니다": "담당 부서 확인이 필요합니다",
    "바로 설치하세요": "확인 전 실행 항목에서 제외하세요",
    "신고만 하면 됩니다": "신고 전 준비 항목을 확인하세요",
    "불가능합니다": "조건에 따라 달라질 수 있습니다",
}


def mask_sensitive_text(text: str) -> str:
    masked = re.sub(r"\b\d{6}-\d{7}\b", "[주민등록번호 마스킹]", text)
    masked = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[이메일 마스킹]", masked)
    masked = re.sub(r"\b01[016789]-?\d{3,4}-?\d{4}\b", "[전화번호 마스킹]", masked)
    return masked


def clean_text(text: str) -> str:
    cleaned = mask_sensitive_text(text)
    for forbidden, replacement in FORBIDDEN_REPLACEMENTS.items():
        cleaned = cleaned.replace(forbidden, replacement)
    return cleaned


def clean_payload(value: Any) -> Any:
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        return [clean_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: clean_payload(item) for key, item in value.items()}
    return value
