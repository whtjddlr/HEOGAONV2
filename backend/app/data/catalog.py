from __future__ import annotations

from typing import Any


FLOW_SCHEMA_VERSION = "2026-06-13"
MAX_TOTAL_QUESTIONS = 10
MAX_ATTEMPTS_PER_FIELD = 2


def option(option_id: str, title: str, exclusive: bool = False) -> dict[str, Any]:
    item = {"id": option_id, "title": title}
    if exclusive:
        item["exclusive"] = True
    return item


def unknown_option() -> dict[str, Any]:
    return {"id": "unknown", "title": "아직 몰라요", "exclusive": True}


QUESTION_BANK = [
    {
        "field": "exact_address",
        "label": "정확한 주소",
        "question": "가게 주소가 정해졌나요?",
        "why": "주소로 관할 부서와 건물 용도를 확인해요.",
        "inputMode": "free_text",
        "required": True,
    },
    {
        "field": "on_site_consumption",
        "label": "매장 취식 여부",
        "question": "매장에서 먹고 갈 수 있나요?",
        "why": "객석 유무에 따라 신고 유형이 달라져요.",
        "inputMode": "single_select",
        "required": True,
        "options": [
            option("yes", "네, 매장 이용 가능"),
            option("no", "아니요, 포장·배달만"),
            unknown_option(),
        ],
    },
    {
        "field": "manufacturing_or_simple_sale",
        "label": "조리·제조 방식",
        "question": "음식이나 디저트를 직접 만드나요?",
        "why": "직접 만드는지에 따라 필요한 신고가 달라져요.",
        "inputMode": "single_select",
        "required": True,
        "options": [
            option("cook", "매장에서 조리"),
            option("make_or_process", "직접 제조·가공"),
            option("finished_goods", "완제품 판매"),
            unknown_option(),
        ],
    },
    {
        "field": "liquor_sales",
        "label": "주류 판매 여부",
        "question": "술도 판매하나요?",
        "why": "주류 판매 여부에 따라 신고 유형이 달라져요.",
        "inputMode": "single_select",
        "required": True,
        "options": [
            option("yes", "네, 판매해요"),
            option("no", "아니요"),
            unknown_option(),
        ],
    },
    {
        "field": "condition_screening",
        "label": "추가 조건",
        "question": "해당되는 항목이 있나요?",
        "why": "있으면 골라주세요. 없으면 해당 없음을 누르세요.",
        "inputMode": "multi_select",
        "required": False,
        "options": [
            option("signage_planned", "간판/옥외광고물"),
            option("outdoor_space_planned", "외부 테이블/보도 사용"),
            option("lpg_use", "LPG 등 가스 사용"),
            option("online_sales_planned", "온라인/택배 판매"),
            option("none", "해당 없음", exclusive=True),
            unknown_option(),
        ],
    },
    {
        "field": "building_use",
        "label": "건축물 용도",
        "question": "건물 용도를 알고 있나요?",
        "why": "모르면 넘어가도 돼요.",
        "inputMode": "free_text",
        "required": True,
    },
    {
        "field": "takeover_type",
        "label": "기존 영업 승계 여부",
        "question": "기존 가게를 인수하나요?",
        "why": "새로 신고할지, 승계할지 확인해요.",
        "inputMode": "single_select",
        "required": False,
        "options": [
            option("transfer", "네, 인수해요"),
            option("new_report", "아니요, 새로 시작해요"),
            unknown_option(),
        ],
    },
]


FIELD_VALUE_MAP = {
    "on_site_consumption": {"yes": True, "no": False},
    "manufacturing_or_simple_sale": {
        "cook": "cook",
        "make_or_process": "manufacturing_or_processing",
        "finished_goods": "resale_or_simple_sale",
    },
    "liquor_sales": {"yes": True, "no": False},
    "condition_screening": {
        "signage_planned": "signage_planned",
        "outdoor_space_planned": "outdoor_space_planned",
        "lpg_use": "lpg_use",
        "online_sales_planned": "online_sales_planned",
        "none": "none",
    },
    "takeover_type": {
        "transfer": "transfer",
        "new_report": "new_report",
    },
}


DOCUMENT_PRIORITY_RULES = [
    {
        "id": "building-ledger",
        "priority": 1,
        "title": "건축물대장 확인",
        "statutoryDeadline": "즉시",
        "perceivedDuration": "즉시",
        "prerequisites": "점포 매물 탐색 완료",
        "unlocks": "임대차계약, 소방필증, 영업신고 검토",
        "reason": "계약 전 건물 용도와 위반 여부를 확인해야 해요.",
    },
    {
        "id": "fire-safety",
        "priority": 2,
        "title": "소방시설완비증명서",
        "statutoryDeadline": "3~7일",
        "perceivedDuration": "5~7일",
        "prerequisites": "임대차계약서, 건축물대장",
        "unlocks": "식품접객업 영업신고증",
        "reason": "대상 여부와 현장 확인 일정이 필요할 수 있어요.",
    },
    {
        "id": "health-check",
        "priority": 3,
        "title": "건강진단결과서",
        "statutoryDeadline": "즉시",
        "perceivedDuration": "4~5일",
        "prerequisites": "창업자 및 종업원 인적사항",
        "unlocks": "식품접객업 영업신고증",
        "reason": "검사 후 결과가 나오기까지 며칠 걸려요.",
    },
    {
        "id": "lpg-certificate",
        "priority": 4,
        "title": "LPG 완성검사필증",
        "statutoryDeadline": "즉시",
        "perceivedDuration": "3~5일",
        "prerequisites": "임대차계약서, 가스 배관 및 화구 시공 완료",
        "unlocks": "식품접객업 영업신고증",
        "reason": "공사 후 검사 일정이 필요해요.",
    },
    {
        "id": "hygiene-education",
        "priority": 5,
        "title": "위생교육 수료증",
        "statutoryDeadline": "즉시",
        "perceivedDuration": "1일",
        "prerequisites": "창업자 인적사항",
        "unlocks": "식품접객업 영업신고증",
        "reason": "신고 전에 수료증이 필요해요.",
    },
    {
        "id": "food-business-report",
        "priority": 6,
        "title": "식품접객업 영업신고증",
        "statutoryDeadline": "즉시",
        "perceivedDuration": "방문 시 즉시",
        "prerequisites": "건축물대장, 보건증, 위생교육 등 선행 서류",
        "unlocks": "사업자등록증, 간판 허가 신청",
        "reason": "앞 서류가 준비돼야 접수할 수 있어요.",
    },
    {
        "id": "business-registration",
        "priority": 7,
        "title": "사업자등록증",
        "statutoryDeadline": "2일 이내",
        "perceivedDuration": "즉시~1일",
        "prerequisites": "영업신고증, 임대차계약서",
        "unlocks": "카드단말기, POS, 세금계산서 등 매출 활동",
        "reason": "영업신고 후 사업자등록을 진행해요.",
    },
    {
        "id": "signage-report",
        "priority": 8,
        "title": "옥외광고물 허가 및 신고증",
        "statutoryDeadline": "7일 이내",
        "perceivedDuration": "3~5일",
        "prerequisites": "사업자등록증, 간판 디자인 도면, 건물 정면도",
        "unlocks": "합법적인 외부 간판 설치",
        "reason": "간판 위치와 크기 기준 확인이 필요해요.",
    },
]
