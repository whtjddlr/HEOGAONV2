from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MINJU_ROOT = ROOT.parent
SCENARIOS_PATH = MINJU_ROOT / "graph_only_scenarios" / "ten_scenario_full_answers.json"

OUT_CATALOG_JSON = ROOT / "form_template_catalog.json"
OUT_CATALOG_MD = ROOT / "form_template_catalog.md"
OUT_SCENARIO_JSON = ROOT / "scenario_form_requirements.json"
OUT_PROMPTS_MD = ROOT / "ai_document_generation_prompts.md"


def field(name: str, description: str, required: bool = True, source: str = "user_input") -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "required": required,
        "source": source,
    }


COMMON_APPLICANT_FIELDS = [
    field("applicant_name", "신청인 또는 대표자 성명"),
    field("applicant_birth_or_registration_no", "생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호"),
    field("applicant_phone", "연락처"),
    field("applicant_address", "주소"),
]

COMMON_BUSINESS_FIELDS = [
    field("business_name", "상호 또는 법인명"),
    field("business_registration_no", "사업자등록번호", False),
    field("business_address", "영업소 또는 사업장 소재지"),
    field("business_phone", "사업장 전화번호", False),
    field("opening_date", "개업 예정일 또는 영업 개시일", False),
]


TEMPLATES: dict[str, dict[str, Any]] = {
    "식품 영업 신고서/영업신고 신청서": {
        "template_id": "food_business_report_application",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "일반음식점·휴게음식점 등 식품접객업 신규 영업신고 신청서. 최종 제출은 관할 보건소/식품위생 담당 창구의 최신 서식을 확인해야 한다.",
        "required_inputs": COMMON_APPLICANT_FIELDS + COMMON_BUSINESS_FIELDS + [
            field("business_type", "업종: 일반음식점영업, 휴게음식점영업, 제과점영업 등"),
            field("business_area_m2", "영업장 면적(㎡)"),
            field("facility_summary", "조리장, 객석, 세척시설 등 시설 개요", False),
            field("uses_lpg", "LPG 사용 여부", False),
            field("is_fire_certificate_target", "소방완비 대상 여부", False),
            field("uses_groundwater", "지하수 사용 여부", False),
            field("has_children_play_facility", "어린이놀이시설 설치 여부", False),
            field("agent_name", "대리 신청인 성명", False),
        ],
        "attachments": ["위생교육수료증", "건강진단결과서", "임대차계약서", "신분증", "LPG 검사필증/필증", "안전시설등 완비증명서/소방완비증명서", "수질검사시험성적서"],
        "cannot_fabricate": ["건강진단결과서", "위생교육수료증", "LPG 검사필증/필증", "안전시설등 완비증명서/소방완비증명서"],
    },
    "사업자등록 신청서": {
        "template_id": "business_registration_application",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "세무서/홈택스 사업자등록 신청서. 인허가 업종은 영업신고증 발급 후 진행하는 흐름으로 둔다.",
        "required_inputs": COMMON_APPLICANT_FIELDS + COMMON_BUSINESS_FIELDS + [
            field("business_category", "업태"),
            field("business_item", "종목"),
            field("lease_start_date", "임대차 시작일", False),
            field("lease_end_date", "임대차 종료일", False),
            field("deposit", "보증금", False),
            field("monthly_rent", "월세", False),
            field("joint_business_partners", "공동사업자 정보", False),
        ],
        "attachments": ["영업신고증", "임대차계약서", "동업계약서"],
        "cannot_fabricate": ["영업신고증"],
    },
    "도로점용허가 신청서": {
        "template_id": "road_occupation_permit_application",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "보도·도로 일부를 테라스, 진입로, 공사용 시설 등으로 점용할 때 쓰는 허가 신청서.",
        "required_inputs": COMMON_APPLICANT_FIELDS + [
            field("occupation_location", "점용 위치 주소 및 지번"),
            field("occupation_purpose", "점용 목적"),
            field("occupation_area_m2", "점용 면적(㎡)"),
            field("occupation_period_start", "점용 시작일"),
            field("occupation_period_end", "점용 종료일"),
            field("structure_or_facility", "설치 시설물 또는 공작물 설명"),
            field("restoration_plan", "원상회복 계획", False),
        ],
        "attachments": ["사업자등록증 사본", "위치도", "위치도 및 평면도", "설계도면", "주요지하매설물 관리자의 의견서", "주요지하매설물의 사후관리계획"],
        "cannot_fabricate": ["사업자등록증 사본", "주요지하매설물 관리자의 의견서"],
    },
    "옥외광고물 표시 신청서": {
        "template_id": "outdoor_ad_display_application",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "벽면이용간판, 돌출간판, 지주이용간판, 입간판 등 옥외광고물 표시 허가·신고 신청서.",
        "required_inputs": COMMON_APPLICANT_FIELDS + COMMON_BUSINESS_FIELDS + [
            field("ad_type", "광고물 종류: 벽면, 돌출, 지주, 입간판 등"),
            field("display_location", "표시 위치"),
            field("ad_width", "가로 길이"),
            field("ad_height", "세로 길이"),
            field("ad_quantity", "수량"),
            field("ad_content", "광고 내용"),
            field("materials", "재질", False),
            field("lighting_method", "조명 방식", False),
            field("installer_name", "광고물 제작·설치업체", False),
        ],
        "attachments": ["소유자/관리자 사용승낙서", "원색사진 또는 원색도안", "설치장소 주변 원색사진", "설계도서", "입간판 도안", "사업자등록증 사본"],
        "cannot_fabricate": ["사업자등록증 사본"],
    },
    "통신판매업 신고서": {
        "template_id": "mail_order_sales_report",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "온라인 판매를 병행할 때 제출하는 통신판매업 신고서.",
        "required_inputs": COMMON_APPLICANT_FIELDS + COMMON_BUSINESS_FIELDS + [
            field("online_store_url", "쇼핑몰/플랫폼/도메인 URL"),
            field("hosting_provider", "호스팅 또는 플랫폼 사업자", False),
            field("sales_items", "판매 품목"),
            field("sales_method", "판매 방식"),
            field("payment_method", "결제 방식"),
            field("escrow_or_purchase_safety", "구매안전서비스 이용 여부", False),
        ],
        "attachments": ["사업자등록증", "대표자 실물신분증", "구매안전서비스 이용확인증"],
        "cannot_fabricate": ["사업자등록증", "대표자 실물신분증", "구매안전서비스 이용확인증"],
    },
    "영업자 지위승계신고서": {
        "template_id": "food_business_succession_report",
        "form_type": "official_application",
        "ai_fill_mode": "fill_official_form",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "기존 음식점 영업을 양도양수 등으로 승계할 때 제출하는 신고서.",
        "required_inputs": [
            field("transferor_name", "양도인 성명/법인명"),
            field("transferor_phone", "양도인 연락처"),
            field("transferee_name", "양수인 성명/법인명"),
            field("transferee_phone", "양수인 연락처"),
            field("business_name", "영업소 명칭"),
            field("business_address", "영업소 소재지"),
            field("succession_reason", "승계 사유: 양도양수, 상속 등"),
            field("succession_date", "승계일"),
            field("license_or_report_no", "기존 영업신고증 번호", False),
        ],
        "attachments": ["기존 영업신고증", "양도양수계약서", "양도인 신분증", "양수인 신분증", "위생교육수료증", "건강진단결과서", "임대차계약서"],
        "cannot_fabricate": ["기존 영업신고증", "양도인 신분증", "양수인 신분증", "위생교육수료증", "건강진단결과서"],
    },
    "양도양수계약서": {
        "template_id": "business_transfer_agreement",
        "form_type": "private_agreement",
        "ai_fill_mode": "draft_private_document",
        "ai_can_prepare": True,
        "risk_level": "high",
        "description": "음식점 영업권, 시설, 비품, 권리금 등을 양도양수하는 계약서 초안. 법률 검토 권장.",
        "required_inputs": [
            field("transferor_name", "양도인"),
            field("transferee_name", "양수인"),
            field("business_name", "대상 영업소"),
            field("business_address", "대상 영업소 주소"),
            field("transfer_assets", "양도 대상 자산과 제외 자산"),
            field("transfer_price", "양도대금"),
            field("deposit_terms", "계약금/중도금/잔금 조건"),
            field("succession_date", "영업 승계일"),
            field("liability_terms", "기존 채무, 행정처분, 민원 책임 분담"),
        ],
        "attachments": ["기존 영업신고증", "임대차계약서"],
        "cannot_fabricate": [],
    },
    "위임장": {
        "template_id": "power_of_attorney",
        "form_type": "private_or_official_attachment",
        "ai_fill_mode": "draft_attachment",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "대리 신청 시 쓰는 위임장 초안.",
        "required_inputs": [
            field("principal_name", "위임인 성명"),
            field("principal_id_or_registration_no", "위임인 식별번호"),
            field("principal_address", "위임인 주소"),
            field("agent_name", "대리인 성명"),
            field("agent_id_or_birth", "대리인 식별정보"),
            field("agent_address", "대리인 주소"),
            field("delegated_task", "위임하는 민원/업무"),
            field("delegation_date", "위임일"),
        ],
        "attachments": ["위임인 신분증 사본", "대리인 신분증"],
        "cannot_fabricate": ["위임인 신분증 사본", "대리인 신분증"],
    },
    "소유자/관리자 사용승낙서": {
        "template_id": "owner_manager_consent_for_sign",
        "form_type": "private_or_official_attachment",
        "ai_fill_mode": "draft_attachment",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "간판을 타인 소유 또는 관리 건물에 표시할 때 필요한 사용승낙서.",
        "required_inputs": [
            field("owner_or_manager_name", "건물주 또는 관리자 성명"),
            field("owner_or_manager_phone", "건물주 또는 관리자 연락처"),
            field("property_address", "건물 주소"),
            field("applicant_name", "광고주 또는 신청인"),
            field("business_name", "상호"),
            field("ad_type", "광고물 종류"),
            field("display_location", "표시 위치"),
            field("consent_period", "승낙 기간", False),
            field("consent_date", "작성일"),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "건물주 동의서 또는 신탁동의서": {
        "template_id": "owner_or_trust_consent_for_food_business",
        "form_type": "private_or_official_attachment",
        "ai_fill_mode": "draft_attachment",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "전대차 또는 신탁 부동산 등에서 영업신고를 위해 동의가 필요한 경우 쓰는 동의서 초안.",
        "required_inputs": [
            field("consenter_name", "건물주, 신탁회사 또는 권한자"),
            field("property_address", "영업장 주소"),
            field("tenant_or_operator", "영업자 또는 임차인"),
            field("business_type", "영업 종류"),
            field("consent_scope", "동의 범위"),
            field("consent_date", "작성일"),
        ],
        "attachments": ["임대차계약서"],
        "cannot_fabricate": [],
    },
    "상담일지": {
        "template_id": "gangnam_food_consultation_note",
        "form_type": "local_official_attachment",
        "ai_fill_mode": "draft_attachment",
        "ai_can_prepare": True,
        "risk_level": "low",
        "description": "강남구 식품접객업 신고 시 지역 서식으로 쓰이는 상담일지 초안.",
        "required_inputs": COMMON_APPLICANT_FIELDS + COMMON_BUSINESS_FIELDS + [
            field("business_type", "영업 종류"),
            field("facility_summary", "시설 개요"),
            field("consultation_notes", "상담 메모", False),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "위치도": {
        "template_id": "location_map_description",
        "form_type": "diagram_or_attachment",
        "ai_fill_mode": "draft_map_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "도로점용 위치를 표시하는 위치도. AI는 설명/도식 초안을 만들 수 있으나 실제 도면 좌표는 사용자가 확인해야 한다.",
        "required_inputs": [
            field("site_address", "점용 위치 주소"),
            field("nearby_landmarks", "인근 기준점"),
            field("road_name", "도로명 또는 보도 위치"),
            field("occupation_area_m2", "점용 면적"),
            field("north_direction", "방위 표시", False),
        ],
        "attachments": ["현장 사진", "평면도"],
        "cannot_fabricate": ["현장 사진"],
    },
    "위치도 및 평면도": {
        "template_id": "location_and_plan_drawing_description",
        "form_type": "diagram_or_attachment",
        "ai_fill_mode": "draft_map_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "도로점용 위치와 면적을 설명하는 위치도/평면도 초안.",
        "required_inputs": [
            field("site_address", "점용 위치 주소"),
            field("site_dimensions", "가로·세로 치수"),
            field("occupation_area_m2", "점용 면적"),
            field("facility_layout", "테라스, 입간판, 시설물 배치"),
            field("pedestrian_clear_width", "보행 가능 폭", False),
        ],
        "attachments": ["현장 사진", "설계도면"],
        "cannot_fabricate": ["현장 사진"],
    },
    "광고물 형상·규격·구조·의장 설명서": {
        "template_id": "ad_shape_spec_description",
        "form_type": "technical_description",
        "ai_fill_mode": "draft_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "광고물의 형상, 규격, 구조, 의장, 재질, 조명방식을 설명하는 첨부 설명서.",
        "required_inputs": [
            field("ad_type", "광고물 종류"),
            field("ad_dimensions", "규격"),
            field("materials", "재질"),
            field("structure_method", "구조/고정 방식"),
            field("design_description", "도안/색상/문구 설명"),
            field("lighting_method", "조명 방식", False),
        ],
        "attachments": ["원색사진 또는 원색도안", "설계도서"],
        "cannot_fabricate": [],
    },
    "원색사진 또는 원색도안": {
        "template_id": "ad_color_design_draft",
        "form_type": "design_attachment",
        "ai_fill_mode": "draft_design_spec",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "광고물 원색도안 초안. 실제 설치장소 원색사진은 사용자가 제공해야 하며, AI는 문구/색상/배치 도안을 작성 보조한다.",
        "required_inputs": [
            field("ad_content", "간판에 표시할 문구"),
            field("brand_logo_or_text", "브랜드 로고 또는 텍스트"),
            field("colors", "주요 색상"),
            field("ad_dimensions", "광고물 규격"),
            field("placement_context", "설치 위치와 주변 환경", False),
            field("reference_image", "참고 이미지", False),
        ],
        "attachments": ["설치장소 주변 원색사진"],
        "cannot_fabricate": ["설치장소 주변 원색사진"],
    },
    "입간판 도안": {
        "template_id": "standing_banner_design_spec",
        "form_type": "design_attachment",
        "ai_fill_mode": "draft_design_spec",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "입간판 길이, 크기, 문구, 색상, 설치 위치를 표시한 도안 또는 사진 대체 설명.",
        "required_inputs": [
            field("banner_width", "입간판 가로 길이"),
            field("banner_height", "입간판 세로/전체 높이"),
            field("ad_content", "표시 문구"),
            field("colors", "색상"),
            field("placement_photo", "설치 위치 사진", False),
        ],
        "attachments": ["사업자등록증 사본", "소유자/관리자 사용승낙서"],
        "cannot_fabricate": ["사업자등록증 사본"],
    },
    "제조ㆍ가공하려는 식품 및 식품첨가물의 종류 및 제조방법설명서": {
        "template_id": "food_manufacturing_method_description",
        "form_type": "technical_description",
        "ai_fill_mode": "draft_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "즉석판매제조가공업 등 제조·가공 영업일 때 필요한 품목 및 제조방법 설명서.",
        "required_inputs": [
            field("product_names", "제조·가공 품목"),
            field("ingredients", "원재료 및 배합"),
            field("process_steps", "제조 공정"),
            field("storage_method", "보관 방법"),
            field("packaging_method", "포장 방식", False),
            field("shelf_life", "소비기한/유통기한", False),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "식품자동판매기의 종류 및 설치장소가 적힌 서류": {
        "template_id": "vending_machine_installation_list",
        "form_type": "attachment_list",
        "ai_fill_mode": "draft_list",
        "ai_can_prepare": True,
        "risk_level": "low",
        "description": "2대 이상 식품자동판매기를 일괄 신고하는 경우 작성하는 기기 종류 및 설치장소 목록.",
        "required_inputs": [
            field("machine_count", "자동판매기 대수"),
            field("machine_types", "자동판매기 종류"),
            field("installation_addresses", "각 설치장소"),
            field("serial_or_management_numbers", "관리번호", False),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "시설사용계약서": {
        "template_id": "facility_use_agreement",
        "form_type": "private_agreement",
        "ai_fill_mode": "draft_private_document",
        "ai_can_prepare": True,
        "risk_level": "high",
        "description": "차고, 세차장, 시설 일부 사용 등 시설 사용 권원을 증명하는 계약서 초안.",
        "required_inputs": [
            field("facility_owner", "시설 제공자"),
            field("facility_user", "시설 사용자"),
            field("facility_address", "시설 위치"),
            field("use_scope", "사용 범위"),
            field("use_period", "사용 기간"),
            field("fee_terms", "사용료 조건", False),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "임대차계약서": {
        "template_id": "lease_agreement_summary",
        "form_type": "private_agreement",
        "ai_fill_mode": "draft_private_document",
        "ai_can_prepare": True,
        "risk_level": "high",
        "description": "점포 임대차계약서 초안 또는 제출용 핵심사항 요약. 실제 계약은 당사자 확인과 법률 검토가 필요하다.",
        "required_inputs": [
            field("lessor_name", "임대인"),
            field("lessee_name", "임차인"),
            field("property_address", "임대 목적물"),
            field("leased_area", "임대 면적", False),
            field("deposit", "보증금"),
            field("monthly_rent", "월세"),
            field("lease_period", "임대차 기간"),
            field("permitted_use", "허용 업종/용도"),
            field("special_terms", "특약", False),
        ],
        "attachments": [],
        "cannot_fabricate": [],
    },
    "도로관리심의회 심의·조정 안전대책 서류": {
        "template_id": "road_safety_measure_plan",
        "form_type": "technical_description",
        "ai_fill_mode": "draft_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "도로굴착 등 심의 대상일 때 안전대책을 정리하는 첨부서류 초안.",
        "required_inputs": [
            field("construction_scope", "공사/점용 범위"),
            field("traffic_safety_plan", "보행자·차량 안전대책"),
            field("construction_period", "공사 기간"),
            field("site_manager", "현장 책임자"),
            field("emergency_contact", "비상 연락처"),
        ],
        "attachments": ["설계도면"],
        "cannot_fabricate": [],
    },
    "주요지하매설물의 사후관리계획": {
        "template_id": "underground_facility_aftercare_plan",
        "form_type": "technical_description",
        "ai_fill_mode": "draft_description",
        "ai_can_prepare": True,
        "risk_level": "medium",
        "description": "도로굴착 후 지하매설물 사후관리계획 초안.",
        "required_inputs": [
            field("facility_type", "지하매설물 종류"),
            field("facility_manager", "관리자"),
            field("inspection_plan", "점검 계획"),
            field("restoration_plan", "복구 및 사후관리 방법"),
            field("emergency_response", "사고 대응 계획"),
        ],
        "attachments": ["설계도면"],
        "cannot_fabricate": [],
    },
}


DEFAULT_CLASSIFICATION = {
    "LPG 검사필증/필증": ("issuer_only", "한국가스안전공사에서 발급받는 증빙"),
    "건강진단결과서": ("issuer_only", "보건소 또는 지정 의료기관 검사 후 발급"),
    "건물 구조안전 확인 서류": ("professional_required", "구조안전 대상이면 전문가 확인 필요"),
    "광고물관리심의위원회 심의관련서류": ("professional_required", "심의대상 여부와 심의자료 확인 필요"),
    "구매안전서비스 이용확인증": ("issuer_only", "은행/PG/플랫폼 등에서 발급"),
    "국유재산 사용허가서": ("issuer_only", "국유재산 관리기관 허가"),
    "기존 영업신고증": ("copy_or_scan", "기존 영업자가 보유한 신고증"),
    "대표자 실물신분증": ("copy_or_scan", "대표자 본인 확인 서류"),
    "대표자 인감도장 및 인감증명서": ("issuer_only", "인감증명서 발급 필요"),
    "도시철도시설 사용계약에 관한 서류": ("issuer_or_contract", "도시철도시설 사용계약 체결 필요"),
    "법인서류": ("issuer_only", "법인등기부등본/법인인감증명서 등 발급"),
    "사업자등록증": ("issuer_only", "세무서/홈택스 발급"),
    "사업자등록증 사본": ("copy_or_scan", "발급된 사업자등록증 사본"),
    "설계도면": ("professional_required", "설계자/시공업체 도면 필요"),
    "설계도서": ("professional_required", "광고업체/설계자 도면 필요"),
    "설치장소 주변 원색사진": ("user_upload", "현장 사진 촬영 필요"),
    "수상레저사업 등록증": ("issuer_only", "해당 등록기관 발급"),
    "수질검사시험성적서": ("issuer_only", "먹는물 수질검사기관 발급"),
    "신분증": ("copy_or_scan", "본인 보유 확인 서류"),
    "안전시설등 완비증명서/소방완비증명서": ("issuer_only", "관할 소방서 현장 확인 후 발급"),
    "양도인 신분증": ("copy_or_scan", "양도인 본인 확인 서류"),
    "양수인 신분증": ("copy_or_scan", "양수인 본인 확인 서류"),
    "어린이놀이시설 검사합격증": ("issuer_only", "검사기관 발급"),
    "영업신고증": ("issuer_only", "관할 식품위생 담당 창구 발급"),
    "예비군식당 운영계약에 관한 서류": ("issuer_or_contract", "계약 당사자/기관 확인 필요"),
    "원색사진 또는 원색도안": ("user_upload_or_ai_assisted", "사진은 사용자가 제공, 도안 설명은 AI 초안 가능"),
    "위생교육수료증": ("issuer_only", "업종별 위생교육기관 수강 후 발급"),
    "유선 또는 도선사업 면허증 또는 신고필증": ("issuer_only", "해당 면허/신고 기관 발급"),
    "전기안전검사필증": ("issuer_only", "한국전기안전공사 등 검사 후 발급"),
    "주요지하매설물 관리자의 의견서": ("issuer_only", "관리자 의견서 필요"),
    "해당 영업장에서 영업을 할 수 있음을 증명하는 식품위생법 시행규칙 별표 15의2에 따른 서류": ("issuer_or_contract", "영업장 사용 가능 증빙 확인 필요"),
}


def load_scenarios() -> list[dict[str, Any]]:
    return json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))


def collect_document_usage(scenarios: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    usage: dict[str, dict[str, Any]] = {}
    for scenario in scenarios:
        for bucket in ["required_documents", "triggered_documents", "conditional_documents"]:
            for doc in scenario.get(bucket, []):
                name = doc["canonical_object"]
                item = usage.setdefault(
                    name,
                    {
                        "document_name": name,
                        "used_in_scenarios": [],
                        "subjects": set(),
                        "source_titles": set(),
                        "source_urls": set(),
                        "issue_or_prepare_at": set(),
                        "submit_to": set(),
                    },
                )
                item["used_in_scenarios"].append({"scenario_id": scenario["scenario_id"], "bucket": bucket})
                item["subjects"].add(doc.get("subject", ""))
                item["source_titles"].add(doc.get("source_title", ""))
                item["source_urls"].add(doc.get("source_url", ""))
                item["issue_or_prepare_at"].add(doc.get("issue_or_prepare_at", ""))
                item["submit_to"].add(doc.get("submit_to", ""))
    for item in usage.values():
        for key in ["subjects", "source_titles", "source_urls", "issue_or_prepare_at", "submit_to"]:
            item[key] = sorted(v for v in item[key] if v)
    return usage


def build_catalog() -> dict[str, Any]:
    scenarios = load_scenarios()
    usage = collect_document_usage(scenarios)
    documents = []
    for name, item in sorted(usage.items()):
        template = TEMPLATES.get(name)
        if template:
            category = "ai_fillable"
            ai_can_prepare = True
            reason = template["description"]
        else:
            category, reason = DEFAULT_CLASSIFICATION.get(name, ("needs_manual_review", "작성/발급 방식 추가 확인 필요"))
            ai_can_prepare = category in {"user_upload_or_ai_assisted"}
        documents.append(
            {
                **item,
                "category": category,
                "ai_can_prepare": ai_can_prepare,
                "classification_reason": reason,
                "template_id": template["template_id"] if template else None,
                "form_type": template["form_type"] if template else None,
                "ai_fill_mode": template["ai_fill_mode"] if template else None,
                "risk_level": template["risk_level"] if template else None,
                "required_inputs": template["required_inputs"] if template else [],
                "attachments": template["attachments"] if template else [],
                "cannot_fabricate": template["cannot_fabricate"] if template else [],
            }
        )
    return {
        "meta": {
            "source": str(SCENARIOS_PATH.relative_to(MINJU_ROOT.parent)),
            "document_count": len(documents),
            "ai_fillable_count": sum(1 for doc in documents if doc["category"] == "ai_fillable"),
            "ai_can_prepare_count": sum(1 for doc in documents if doc["ai_can_prepare"]),
            "generated_for": "허가온 10개 시연 시나리오의 필요서류 작성 자동화",
        },
        "documents": documents,
    }


def build_scenario_requirements(catalog: dict[str, Any]) -> dict[str, Any]:
    docs_by_name = {doc["document_name"]: doc for doc in catalog["documents"]}
    scenarios = load_scenarios()
    result = []
    for scenario in scenarios:
        fillable_now = []
        fillable_conditional = []
        evidence_now = []
        evidence_conditional = []
        seen: set[tuple[str, str, str]] = set()
        for bucket in ["required_documents", "triggered_documents", "conditional_documents"]:
            for doc in scenario.get(bucket, []):
                catalog_doc = docs_by_name[doc["canonical_object"]]
                key = (doc["canonical_object"], bucket, doc.get("subject", ""))
                if key in seen:
                    continue
                seen.add(key)
                row = {
                    "document_name": doc["canonical_object"],
                    "bucket": bucket,
                    "category": catalog_doc["category"],
                    "template_id": catalog_doc["template_id"],
                    "issue_or_prepare_at": doc.get("issue_or_prepare_at", ""),
                    "submit_to": doc.get("submit_to", ""),
                }
                is_now = bucket in {"required_documents", "triggered_documents"}
                if catalog_doc["ai_can_prepare"] and is_now:
                    fillable_now.append(row)
                elif catalog_doc["ai_can_prepare"]:
                    fillable_conditional.append(row)
                elif is_now:
                    evidence_now.append(row)
                else:
                    evidence_conditional.append(row)
        result.append(
            {
                "scenario_id": scenario["scenario_id"],
                "input": scenario["input"],
                "ai_fillable_now": fillable_now,
                "ai_fillable_if_condition_applies": fillable_conditional,
                "issuer_or_attachment_now": evidence_now,
                "issuer_or_attachment_if_condition_applies": evidence_conditional,
            }
        )
    return {"scenarios": result}


def write_markdown(catalog: dict[str, Any]) -> None:
    lines = [
        "# AI 작성용 양식 카탈로그",
        "",
        "10개 시나리오의 필요서류를 기준으로, AI가 대신 작성할 수 있는 양식과 반드시 기관에서 발급받아야 하는 증빙을 분리했습니다.",
        "",
        "## 원칙",
        "",
        "- AI 작성 가능: 신청서, 신고서, 위임장, 승낙서, 계약서 초안, 위치도/설명서류 초안",
        "- AI 작성 불가: 신분증, 보건증, 위생교육수료증, 영업신고증, 사업자등록증, 소방완비증명서, LPG 검사필증 등 기관 발급 증빙",
        "- 실제 제출 전에는 관할 기관 최신 서식과 담당자 확인이 필요합니다.",
        "",
        "## AI 작성 가능한 양식",
        "",
    ]
    for doc in catalog["documents"]:
        if doc["category"] != "ai_fillable":
            continue
        lines.extend(
            [
                f"### {doc['document_name']}",
                "",
                f"- template_id: `{doc['template_id']}`",
                f"- form_type: `{doc['form_type']}`",
                f"- 작성 방식: `{doc['ai_fill_mode']}`",
                f"- 위험도: `{doc['risk_level']}`",
                f"- 설명: {doc['classification_reason']}",
                f"- 사용 시나리오: {', '.join(sorted({row['scenario_id'] for row in doc['used_in_scenarios']}))}",
                "",
                "필요 입력값:",
            ]
        )
        for f in doc["required_inputs"]:
            required = "필수" if f["required"] else "선택"
            lines.append(f"- `{f['name']}` ({required}): {f['description']}")
        if doc["attachments"]:
            lines.append("")
            lines.append("첨부/선행 증빙:")
            for attachment in doc["attachments"]:
                marker = "AI 작성 금지" if attachment in doc["cannot_fabricate"] else "첨부 또는 초안 가능"
                lines.append(f"- {attachment}: {marker}")
        lines.append("")

    lines.extend(["## 기관 발급/첨부 전용 서류", ""])
    for doc in catalog["documents"]:
        if doc["category"] == "ai_fillable":
            continue
        lines.append(f"- **{doc['document_name']}**: `{doc['category']}` / {doc['classification_reason']}")
    OUT_CATALOG_MD.write_text("\n".join(lines), encoding="utf-8")


def write_prompts(catalog: dict[str, Any]) -> None:
    lines = [
        "# AI 문서 작성 프롬프트 템플릿",
        "",
        "아래 템플릿은 `form_template_catalog.json`의 `template_id`와 입력 필드를 사용해 문서 초안을 만들 때 사용합니다.",
        "",
        "## 공통 시스템 규칙",
        "",
        "```text",
        "너는 행정서류 작성 보조자다. 사용자가 제공한 사실만 양식에 기입한다. 모르는 값은 추측하지 말고 [확인 필요]로 남긴다. 기관 발급 증빙, 신분증, 보건증, 수료증, 필증, 신고증, 사업자등록증은 생성하지 않는다. 최종 제출 전 최신 공식 서식과 관할 기관 확인이 필요하다고 표시한다.",
        "```",
        "",
    ]
    for doc in catalog["documents"]:
        if doc["category"] != "ai_fillable":
            continue
        field_names = ", ".join(f["name"] for f in doc["required_inputs"])
        lines.extend(
            [
                f"## {doc['document_name']}",
                "",
                "```text",
                f"template_id: {doc['template_id']}",
                f"문서명: {doc['document_name']}",
                f"작성 방식: {doc['ai_fill_mode']}",
                f"필요 입력값: {field_names}",
                "요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.",
                "```",
                "",
            ]
        )
    OUT_PROMPTS_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog()
    OUT_CATALOG_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_SCENARIO_JSON.write_text(json.dumps(build_scenario_requirements(catalog), ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(catalog)
    write_prompts(catalog)
    print(f"documents={catalog['meta']['document_count']} ai_fillable={catalog['meta']['ai_fillable_count']}")
    print(f"catalog_json={OUT_CATALOG_JSON}")
    print(f"catalog_md={OUT_CATALOG_MD}")
    print(f"scenario_json={OUT_SCENARIO_JSON}")
    print(f"prompts_md={OUT_PROMPTS_MD}")


if __name__ == "__main__":
    main()
