from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_slot(
    case: dict[str, Any],
    field: str,
    value: Any,
    user_text: str,
    admin_term: str,
    status: str = "known",
) -> None:
    case["slots"][field] = {
        "field": field,
        "value": value,
        "userText": user_text,
        "adminTerm": admin_term,
        "status": status,
        "updatedAt": now_iso(),
    }


def append_condition(case: dict[str, Any], value: str) -> None:
    current = as_list(slot_value(case, "condition_screening"))
    if value not in current:
        current.append(value)
    set_slot(case, "condition_screening", current, condition_user_text(current), "추가 조건 스크리닝")


def slot_value(case: dict[str, Any], field: str) -> Any:
    slot = case["slots"].get(field)
    if not slot:
        return None
    return slot.get("value")


def slot_known(case: dict[str, Any], field: str) -> bool:
    value = slot_value(case, field)
    return value not in (None, "", "unknown", [])


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def append_unique(items: list[Any], value: Any) -> None:
    if value not in items:
        items.append(value)


def admin_term_for(field: str, value: Any) -> str:
    if field == "on_site_consumption":
        return "객석 있음 / 식품접객업 검토" if value is True else "객석 없음 / 포장·배달 검토"
    if field == "manufacturing_or_simple_sale":
        return {
            "cook": "매장 조리",
            "manufacturing_or_processing": "제조·가공",
            "resale_or_simple_sale": "완제품 단순 판매",
        }.get(str(value), "조리·제조 방식")
    if field == "liquor_sales":
        return "주류 판매 검토" if value is True else "주류 판매 없음"
    if field == "condition_screening":
        return "추가 조건 스크리닝"
    if field == "building_use":
        return "건축물대장상 용도"
    if field == "exact_address":
        return "도로명/지번 주소"
    return label_for_field(field)


def condition_user_text(values: list[Any]) -> str:
    labels = {
        "signage_planned": "간판/옥외광고물",
        "outdoor_space_planned": "외부 테이블/보도 사용",
        "lpg_use": "LPG 등 가스 사용",
        "online_sales_planned": "온라인/택배 판매",
        "none": "해당 없음",
    }
    return " + ".join(labels.get(str(value), str(value)) for value in values)


def label_for_field(field: str) -> str:
    labels = {
        "exact_address": "정확한 주소",
        "building_use": "건축물 용도",
        "on_site_consumption": "매장 취식 여부",
        "manufacturing_or_simple_sale": "조리·제조 방식",
        "liquor_sales": "주류 판매 여부",
        "condition_screening": "간판·외부공간·가스 등 추가 조건",
        "takeover_type": "기존 영업 승계 여부",
    }
    return labels.get(field, field)
