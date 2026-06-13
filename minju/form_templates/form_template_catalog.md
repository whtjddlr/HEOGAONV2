# AI 작성용 양식 카탈로그

10개 시나리오의 필요서류를 기준으로, AI가 대신 작성할 수 있는 양식과 반드시 기관에서 발급받아야 하는 증빙을 분리했습니다.

## 원칙

- AI 작성 가능: 신청서, 신고서, 위임장, 승낙서, 계약서 초안, 위치도/설명서류 초안
- AI 작성 불가: 신분증, 보건증, 위생교육수료증, 영업신고증, 사업자등록증, 소방완비증명서, LPG 검사필증 등 기관 발급 증빙
- 실제 제출 전에는 관할 기관 최신 서식과 담당자 확인이 필요합니다.

## AI 작성 가능한 양식

### 건물주 동의서 또는 신탁동의서

- template_id: `owner_or_trust_consent_for_food_business`
- form_type: `private_or_official_attachment`
- 작성 방식: `draft_attachment`
- 위험도: `medium`
- 설명: 전대차 또는 신탁 부동산 등에서 영업신고를 위해 동의가 필요한 경우 쓰는 동의서 초안.
- 사용 시나리오: s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `consenter_name` (필수): 건물주, 신탁회사 또는 권한자
- `property_address` (필수): 영업장 주소
- `tenant_or_operator` (필수): 영업자 또는 임차인
- `business_type` (필수): 영업 종류
- `consent_scope` (필수): 동의 범위
- `consent_date` (필수): 작성일

첨부/선행 증빙:
- 임대차계약서: 첨부 또는 초안 가능

### 광고물 형상·규격·구조·의장 설명서

- template_id: `ad_shape_spec_description`
- form_type: `technical_description`
- 작성 방식: `draft_description`
- 위험도: `medium`
- 설명: 광고물의 형상, 규격, 구조, 의장, 재질, 조명방식을 설명하는 첨부 설명서.
- 사용 시나리오: s07_songpa_fixed_sign

필요 입력값:
- `ad_type` (필수): 광고물 종류
- `ad_dimensions` (필수): 규격
- `materials` (필수): 재질
- `structure_method` (필수): 구조/고정 방식
- `design_description` (필수): 도안/색상/문구 설명
- `lighting_method` (선택): 조명 방식

첨부/선행 증빙:
- 원색사진 또는 원색도안: 첨부 또는 초안 가능
- 설계도서: 첨부 또는 초안 가능

### 도로관리심의회 심의·조정 안전대책 서류

- template_id: `road_safety_measure_plan`
- form_type: `technical_description`
- 작성 방식: `draft_description`
- 위험도: `medium`
- 설명: 도로굴착 등 심의 대상일 때 안전대책을 정리하는 첨부서류 초안.
- 사용 시나리오: s05_gangnam_restaurant_road_terrace

필요 입력값:
- `construction_scope` (필수): 공사/점용 범위
- `traffic_safety_plan` (필수): 보행자·차량 안전대책
- `construction_period` (필수): 공사 기간
- `site_manager` (필수): 현장 책임자
- `emergency_contact` (필수): 비상 연락처

첨부/선행 증빙:
- 설계도면: 첨부 또는 초안 가능

### 도로점용허가 신청서

- template_id: `road_occupation_permit_application`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 보도·도로 일부를 테라스, 진입로, 공사용 시설 등으로 점용할 때 쓰는 허가 신청서.
- 사용 시나리오: s05_gangnam_restaurant_road_terrace

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `occupation_location` (필수): 점용 위치 주소 및 지번
- `occupation_purpose` (필수): 점용 목적
- `occupation_area_m2` (필수): 점용 면적(㎡)
- `occupation_period_start` (필수): 점용 시작일
- `occupation_period_end` (필수): 점용 종료일
- `structure_or_facility` (필수): 설치 시설물 또는 공작물 설명
- `restoration_plan` (선택): 원상회복 계획

첨부/선행 증빙:
- 사업자등록증 사본: AI 작성 금지
- 위치도: 첨부 또는 초안 가능
- 위치도 및 평면도: 첨부 또는 초안 가능
- 설계도면: 첨부 또는 초안 가능
- 주요지하매설물 관리자의 의견서: AI 작성 금지
- 주요지하매설물의 사후관리계획: 첨부 또는 초안 가능

### 사업자등록 신청서

- template_id: `business_registration_application`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 세무서/홈택스 사업자등록 신청서. 인허가 업종은 영업신고증 발급 후 진행하는 흐름으로 둔다.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater, s10_gangnam_online_sales

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `business_name` (필수): 상호 또는 법인명
- `business_registration_no` (선택): 사업자등록번호
- `business_address` (필수): 영업소 또는 사업장 소재지
- `business_phone` (선택): 사업장 전화번호
- `opening_date` (선택): 개업 예정일 또는 영업 개시일
- `business_category` (필수): 업태
- `business_item` (필수): 종목
- `lease_start_date` (선택): 임대차 시작일
- `lease_end_date` (선택): 임대차 종료일
- `deposit` (선택): 보증금
- `monthly_rent` (선택): 월세
- `joint_business_partners` (선택): 공동사업자 정보

첨부/선행 증빙:
- 영업신고증: AI 작성 금지
- 임대차계약서: 첨부 또는 초안 가능
- 동업계약서: 첨부 또는 초안 가능

### 상담일지

- template_id: `gangnam_food_consultation_note`
- form_type: `local_official_attachment`
- 작성 방식: `draft_attachment`
- 위험도: `low`
- 설명: 강남구 식품접객업 신고 시 지역 서식으로 쓰이는 상담일지 초안.
- 사용 시나리오: s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `business_name` (필수): 상호 또는 법인명
- `business_registration_no` (선택): 사업자등록번호
- `business_address` (필수): 영업소 또는 사업장 소재지
- `business_phone` (선택): 사업장 전화번호
- `opening_date` (선택): 개업 예정일 또는 영업 개시일
- `business_type` (필수): 영업 종류
- `facility_summary` (필수): 시설 개요
- `consultation_notes` (선택): 상담 메모

### 소유자/관리자 사용승낙서

- template_id: `owner_manager_consent_for_sign`
- form_type: `private_or_official_attachment`
- 작성 방식: `draft_attachment`
- 위험도: `medium`
- 설명: 간판을 타인 소유 또는 관리 건물에 표시할 때 필요한 사용승낙서.
- 사용 시나리오: s07_songpa_fixed_sign, s08_songpa_standing_banner

필요 입력값:
- `owner_or_manager_name` (필수): 건물주 또는 관리자 성명
- `owner_or_manager_phone` (필수): 건물주 또는 관리자 연락처
- `property_address` (필수): 건물 주소
- `applicant_name` (필수): 광고주 또는 신청인
- `business_name` (필수): 상호
- `ad_type` (필수): 광고물 종류
- `display_location` (필수): 표시 위치
- `consent_period` (선택): 승낙 기간
- `consent_date` (필수): 작성일

### 시설사용계약서

- template_id: `facility_use_agreement`
- form_type: `private_agreement`
- 작성 방식: `draft_private_document`
- 위험도: `high`
- 설명: 차고, 세차장, 시설 일부 사용 등 시설 사용 권원을 증명하는 계약서 초안.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `facility_owner` (필수): 시설 제공자
- `facility_user` (필수): 시설 사용자
- `facility_address` (필수): 시설 위치
- `use_scope` (필수): 사용 범위
- `use_period` (필수): 사용 기간
- `fee_terms` (선택): 사용료 조건

### 식품 영업 신고서/영업신고 신청서

- template_id: `food_business_report_application`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 일반음식점·휴게음식점 등 식품접객업 신규 영업신고 신청서. 최종 제출은 관할 보건소/식품위생 담당 창구의 최신 서식을 확인해야 한다.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `business_name` (필수): 상호 또는 법인명
- `business_registration_no` (선택): 사업자등록번호
- `business_address` (필수): 영업소 또는 사업장 소재지
- `business_phone` (선택): 사업장 전화번호
- `opening_date` (선택): 개업 예정일 또는 영업 개시일
- `business_type` (필수): 업종: 일반음식점영업, 휴게음식점영업, 제과점영업 등
- `business_area_m2` (필수): 영업장 면적(㎡)
- `facility_summary` (선택): 조리장, 객석, 세척시설 등 시설 개요
- `uses_lpg` (선택): LPG 사용 여부
- `is_fire_certificate_target` (선택): 소방완비 대상 여부
- `uses_groundwater` (선택): 지하수 사용 여부
- `has_children_play_facility` (선택): 어린이놀이시설 설치 여부
- `agent_name` (선택): 대리 신청인 성명

첨부/선행 증빙:
- 위생교육수료증: AI 작성 금지
- 건강진단결과서: AI 작성 금지
- 임대차계약서: 첨부 또는 초안 가능
- 신분증: 첨부 또는 초안 가능
- LPG 검사필증/필증: AI 작성 금지
- 안전시설등 완비증명서/소방완비증명서: AI 작성 금지
- 수질검사시험성적서: 첨부 또는 초안 가능

### 식품자동판매기의 종류 및 설치장소가 적힌 서류

- template_id: `vending_machine_installation_list`
- form_type: `attachment_list`
- 작성 방식: `draft_list`
- 위험도: `low`
- 설명: 2대 이상 식품자동판매기를 일괄 신고하는 경우 작성하는 기기 종류 및 설치장소 목록.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `machine_count` (필수): 자동판매기 대수
- `machine_types` (필수): 자동판매기 종류
- `installation_addresses` (필수): 각 설치장소
- `serial_or_management_numbers` (선택): 관리번호

### 양도양수계약서

- template_id: `business_transfer_agreement`
- form_type: `private_agreement`
- 작성 방식: `draft_private_document`
- 위험도: `high`
- 설명: 음식점 영업권, 시설, 비품, 권리금 등을 양도양수하는 계약서 초안. 법률 검토 권장.
- 사용 시나리오: s09_gangnam_food_succession

필요 입력값:
- `transferor_name` (필수): 양도인
- `transferee_name` (필수): 양수인
- `business_name` (필수): 대상 영업소
- `business_address` (필수): 대상 영업소 주소
- `transfer_assets` (필수): 양도 대상 자산과 제외 자산
- `transfer_price` (필수): 양도대금
- `deposit_terms` (필수): 계약금/중도금/잔금 조건
- `succession_date` (필수): 영업 승계일
- `liability_terms` (필수): 기존 채무, 행정처분, 민원 책임 분담

첨부/선행 증빙:
- 기존 영업신고증: 첨부 또는 초안 가능
- 임대차계약서: 첨부 또는 초안 가능

### 영업자 지위승계신고서

- template_id: `food_business_succession_report`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 기존 음식점 영업을 양도양수 등으로 승계할 때 제출하는 신고서.
- 사용 시나리오: s09_gangnam_food_succession

필요 입력값:
- `transferor_name` (필수): 양도인 성명/법인명
- `transferor_phone` (필수): 양도인 연락처
- `transferee_name` (필수): 양수인 성명/법인명
- `transferee_phone` (필수): 양수인 연락처
- `business_name` (필수): 영업소 명칭
- `business_address` (필수): 영업소 소재지
- `succession_reason` (필수): 승계 사유: 양도양수, 상속 등
- `succession_date` (필수): 승계일
- `license_or_report_no` (선택): 기존 영업신고증 번호

첨부/선행 증빙:
- 기존 영업신고증: AI 작성 금지
- 양도양수계약서: 첨부 또는 초안 가능
- 양도인 신분증: AI 작성 금지
- 양수인 신분증: AI 작성 금지
- 위생교육수료증: AI 작성 금지
- 건강진단결과서: AI 작성 금지
- 임대차계약서: 첨부 또는 초안 가능

### 옥외광고물 표시 신청서

- template_id: `outdoor_ad_display_application`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 벽면이용간판, 돌출간판, 지주이용간판, 입간판 등 옥외광고물 표시 허가·신고 신청서.
- 사용 시나리오: s07_songpa_fixed_sign, s08_songpa_standing_banner

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `business_name` (필수): 상호 또는 법인명
- `business_registration_no` (선택): 사업자등록번호
- `business_address` (필수): 영업소 또는 사업장 소재지
- `business_phone` (선택): 사업장 전화번호
- `opening_date` (선택): 개업 예정일 또는 영업 개시일
- `ad_type` (필수): 광고물 종류: 벽면, 돌출, 지주, 입간판 등
- `display_location` (필수): 표시 위치
- `ad_width` (필수): 가로 길이
- `ad_height` (필수): 세로 길이
- `ad_quantity` (필수): 수량
- `ad_content` (필수): 광고 내용
- `materials` (선택): 재질
- `lighting_method` (선택): 조명 방식
- `installer_name` (선택): 광고물 제작·설치업체

첨부/선행 증빙:
- 소유자/관리자 사용승낙서: 첨부 또는 초안 가능
- 원색사진 또는 원색도안: 첨부 또는 초안 가능
- 설치장소 주변 원색사진: 첨부 또는 초안 가능
- 설계도서: 첨부 또는 초안 가능
- 입간판 도안: 첨부 또는 초안 가능
- 사업자등록증 사본: AI 작성 금지

### 원색사진 또는 원색도안

- template_id: `ad_color_design_draft`
- form_type: `design_attachment`
- 작성 방식: `draft_design_spec`
- 위험도: `medium`
- 설명: 광고물 원색도안 초안. 실제 설치장소 원색사진은 사용자가 제공해야 하며, AI는 문구/색상/배치 도안을 작성 보조한다.
- 사용 시나리오: s07_songpa_fixed_sign

필요 입력값:
- `ad_content` (필수): 간판에 표시할 문구
- `brand_logo_or_text` (필수): 브랜드 로고 또는 텍스트
- `colors` (필수): 주요 색상
- `ad_dimensions` (필수): 광고물 규격
- `placement_context` (선택): 설치 위치와 주변 환경
- `reference_image` (선택): 참고 이미지

첨부/선행 증빙:
- 설치장소 주변 원색사진: AI 작성 금지

### 위임장

- template_id: `power_of_attorney`
- form_type: `private_or_official_attachment`
- 작성 방식: `draft_attachment`
- 위험도: `medium`
- 설명: 대리 신청 시 쓰는 위임장 초안.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire

필요 입력값:
- `principal_name` (필수): 위임인 성명
- `principal_id_or_registration_no` (필수): 위임인 식별번호
- `principal_address` (필수): 위임인 주소
- `agent_name` (필수): 대리인 성명
- `agent_id_or_birth` (필수): 대리인 식별정보
- `agent_address` (필수): 대리인 주소
- `delegated_task` (필수): 위임하는 민원/업무
- `delegation_date` (필수): 위임일

첨부/선행 증빙:
- 위임인 신분증 사본: AI 작성 금지
- 대리인 신분증: AI 작성 금지

### 위치도

- template_id: `location_map_description`
- form_type: `diagram_or_attachment`
- 작성 방식: `draft_map_description`
- 위험도: `medium`
- 설명: 도로점용 위치를 표시하는 위치도. AI는 설명/도식 초안을 만들 수 있으나 실제 도면 좌표는 사용자가 확인해야 한다.
- 사용 시나리오: s05_gangnam_restaurant_road_terrace

필요 입력값:
- `site_address` (필수): 점용 위치 주소
- `nearby_landmarks` (필수): 인근 기준점
- `road_name` (필수): 도로명 또는 보도 위치
- `occupation_area_m2` (필수): 점용 면적
- `north_direction` (선택): 방위 표시

첨부/선행 증빙:
- 현장 사진: AI 작성 금지
- 평면도: 첨부 또는 초안 가능

### 임대차계약서

- template_id: `lease_agreement_summary`
- form_type: `private_agreement`
- 작성 방식: `draft_private_document`
- 위험도: `high`
- 설명: 점포 임대차계약서 초안 또는 제출용 핵심사항 요약. 실제 계약은 당사자 확인과 법률 검토가 필요하다.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater, s09_gangnam_food_succession, s10_gangnam_online_sales

필요 입력값:
- `lessor_name` (필수): 임대인
- `lessee_name` (필수): 임차인
- `property_address` (필수): 임대 목적물
- `leased_area` (선택): 임대 면적
- `deposit` (필수): 보증금
- `monthly_rent` (필수): 월세
- `lease_period` (필수): 임대차 기간
- `permitted_use` (필수): 허용 업종/용도
- `special_terms` (선택): 특약

### 입간판 도안

- template_id: `standing_banner_design_spec`
- form_type: `design_attachment`
- 작성 방식: `draft_design_spec`
- 위험도: `medium`
- 설명: 입간판 길이, 크기, 문구, 색상, 설치 위치를 표시한 도안 또는 사진 대체 설명.
- 사용 시나리오: s08_songpa_standing_banner

필요 입력값:
- `banner_width` (필수): 입간판 가로 길이
- `banner_height` (필수): 입간판 세로/전체 높이
- `ad_content` (필수): 표시 문구
- `colors` (필수): 색상
- `placement_photo` (선택): 설치 위치 사진

첨부/선행 증빙:
- 사업자등록증 사본: AI 작성 금지
- 소유자/관리자 사용승낙서: 첨부 또는 초안 가능

### 제조ㆍ가공하려는 식품 및 식품첨가물의 종류 및 제조방법설명서

- template_id: `food_manufacturing_method_description`
- form_type: `technical_description`
- 작성 방식: `draft_description`
- 위험도: `medium`
- 설명: 즉석판매제조가공업 등 제조·가공 영업일 때 필요한 품목 및 제조방법 설명서.
- 사용 시나리오: s01_mapo_cafe_basic, s02_mapo_cafe_lpg, s03_mapo_cafe_basement_fire, s04_gangnam_restaurant_basic, s05_gangnam_restaurant_road_terrace, s06_gangnam_restaurant_groundwater

필요 입력값:
- `product_names` (필수): 제조·가공 품목
- `ingredients` (필수): 원재료 및 배합
- `process_steps` (필수): 제조 공정
- `storage_method` (필수): 보관 방법
- `packaging_method` (선택): 포장 방식
- `shelf_life` (선택): 소비기한/유통기한

### 주요지하매설물의 사후관리계획

- template_id: `underground_facility_aftercare_plan`
- form_type: `technical_description`
- 작성 방식: `draft_description`
- 위험도: `medium`
- 설명: 도로굴착 후 지하매설물 사후관리계획 초안.
- 사용 시나리오: s05_gangnam_restaurant_road_terrace

필요 입력값:
- `facility_type` (필수): 지하매설물 종류
- `facility_manager` (필수): 관리자
- `inspection_plan` (필수): 점검 계획
- `restoration_plan` (필수): 복구 및 사후관리 방법
- `emergency_response` (필수): 사고 대응 계획

첨부/선행 증빙:
- 설계도면: 첨부 또는 초안 가능

### 통신판매업 신고서

- template_id: `mail_order_sales_report`
- form_type: `official_application`
- 작성 방식: `fill_official_form`
- 위험도: `medium`
- 설명: 온라인 판매를 병행할 때 제출하는 통신판매업 신고서.
- 사용 시나리오: s10_gangnam_online_sales

필요 입력값:
- `applicant_name` (필수): 신청인 또는 대표자 성명
- `applicant_birth_or_registration_no` (필수): 생년월일, 주민등록번호 앞자리, 사업자등록번호 등 양식이 요구하는 식별번호
- `applicant_phone` (필수): 연락처
- `applicant_address` (필수): 주소
- `business_name` (필수): 상호 또는 법인명
- `business_registration_no` (선택): 사업자등록번호
- `business_address` (필수): 영업소 또는 사업장 소재지
- `business_phone` (선택): 사업장 전화번호
- `opening_date` (선택): 개업 예정일 또는 영업 개시일
- `online_store_url` (필수): 쇼핑몰/플랫폼/도메인 URL
- `hosting_provider` (선택): 호스팅 또는 플랫폼 사업자
- `sales_items` (필수): 판매 품목
- `sales_method` (필수): 판매 방식
- `payment_method` (필수): 결제 방식
- `escrow_or_purchase_safety` (선택): 구매안전서비스 이용 여부

첨부/선행 증빙:
- 사업자등록증: AI 작성 금지
- 대표자 실물신분증: AI 작성 금지
- 구매안전서비스 이용확인증: AI 작성 금지

## 기관 발급/첨부 전용 서류

- **LPG 검사필증/필증**: `issuer_only` / 한국가스안전공사에서 발급받는 증빙
- **건강진단결과서**: `issuer_only` / 보건소 또는 지정 의료기관 검사 후 발급
- **건물 구조안전 확인 서류**: `professional_required` / 구조안전 대상이면 전문가 확인 필요
- **광고물관리심의위원회 심의관련서류**: `professional_required` / 심의대상 여부와 심의자료 확인 필요
- **구매안전서비스 이용확인증**: `issuer_only` / 은행/PG/플랫폼 등에서 발급
- **국유재산 사용허가서**: `issuer_only` / 국유재산 관리기관 허가
- **기존 영업신고증**: `copy_or_scan` / 기존 영업자가 보유한 신고증
- **대표자 실물신분증**: `copy_or_scan` / 대표자 본인 확인 서류
- **대표자 인감도장 및 인감증명서**: `issuer_only` / 인감증명서 발급 필요
- **도시철도시설 사용계약에 관한 서류**: `issuer_or_contract` / 도시철도시설 사용계약 체결 필요
- **법인서류**: `issuer_only` / 법인등기부등본/법인인감증명서 등 발급
- **사업자등록증**: `issuer_only` / 세무서/홈택스 발급
- **사업자등록증 사본**: `copy_or_scan` / 발급된 사업자등록증 사본
- **설계도면**: `professional_required` / 설계자/시공업체 도면 필요
- **설계도서**: `professional_required` / 광고업체/설계자 도면 필요
- **설치장소 주변 원색사진**: `user_upload` / 현장 사진 촬영 필요
- **수상레저사업 등록증**: `issuer_only` / 해당 등록기관 발급
- **수질검사시험성적서**: `issuer_only` / 먹는물 수질검사기관 발급
- **신분증**: `copy_or_scan` / 본인 보유 확인 서류
- **안전시설등 완비증명서/소방완비증명서**: `issuer_only` / 관할 소방서 현장 확인 후 발급
- **양도인 신분증**: `copy_or_scan` / 양도인 본인 확인 서류
- **양수인 신분증**: `copy_or_scan` / 양수인 본인 확인 서류
- **어린이놀이시설 검사합격증**: `issuer_only` / 검사기관 발급
- **영업신고증**: `issuer_only` / 관할 식품위생 담당 창구 발급
- **예비군식당 운영계약에 관한 서류**: `issuer_or_contract` / 계약 당사자/기관 확인 필요
- **위생교육수료증**: `issuer_only` / 업종별 위생교육기관 수강 후 발급
- **유선 또는 도선사업 면허증 또는 신고필증**: `issuer_only` / 해당 면허/신고 기관 발급
- **전기안전검사필증**: `issuer_only` / 한국전기안전공사 등 검사 후 발급
- **주요지하매설물 관리자의 의견서**: `issuer_only` / 관리자 의견서 필요
- **해당 영업장에서 영업을 할 수 있음을 증명하는 식품위생법 시행규칙 별표 15의2에 따른 서류**: `issuer_or_contract` / 영업장 사용 가능 증빙 확인 필요