# AI 문서 작성 프롬프트 템플릿

아래 템플릿은 `form_template_catalog.json`의 `template_id`와 입력 필드를 사용해 문서 초안을 만들 때 사용합니다.

## 공통 시스템 규칙

```text
너는 행정서류 작성 보조자다. 사용자가 제공한 사실만 양식에 기입한다. 모르는 값은 추측하지 말고 [확인 필요]로 남긴다. 기관 발급 증빙, 신분증, 보건증, 수료증, 필증, 신고증, 사업자등록증은 생성하지 않는다. 최종 제출 전 최신 공식 서식과 관할 기관 확인이 필요하다고 표시한다.
```

## 건물주 동의서 또는 신탁동의서

```text
template_id: owner_or_trust_consent_for_food_business
문서명: 건물주 동의서 또는 신탁동의서
작성 방식: draft_attachment
필요 입력값: consenter_name, property_address, tenant_or_operator, business_type, consent_scope, consent_date
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 광고물 형상·규격·구조·의장 설명서

```text
template_id: ad_shape_spec_description
문서명: 광고물 형상·규격·구조·의장 설명서
작성 방식: draft_description
필요 입력값: ad_type, ad_dimensions, materials, structure_method, design_description, lighting_method
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 도로관리심의회 심의·조정 안전대책 서류

```text
template_id: road_safety_measure_plan
문서명: 도로관리심의회 심의·조정 안전대책 서류
작성 방식: draft_description
필요 입력값: construction_scope, traffic_safety_plan, construction_period, site_manager, emergency_contact
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 도로점용허가 신청서

```text
template_id: road_occupation_permit_application
문서명: 도로점용허가 신청서
작성 방식: fill_official_form
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, occupation_location, occupation_purpose, occupation_area_m2, occupation_period_start, occupation_period_end, structure_or_facility, restoration_plan
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 사업자등록 신청서

```text
template_id: business_registration_application
문서명: 사업자등록 신청서
작성 방식: fill_official_form
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, business_name, business_registration_no, business_address, business_phone, opening_date, business_category, business_item, lease_start_date, lease_end_date, deposit, monthly_rent, joint_business_partners
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 상담일지

```text
template_id: gangnam_food_consultation_note
문서명: 상담일지
작성 방식: draft_attachment
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, business_name, business_registration_no, business_address, business_phone, opening_date, business_type, facility_summary, consultation_notes
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 소유자/관리자 사용승낙서

```text
template_id: owner_manager_consent_for_sign
문서명: 소유자/관리자 사용승낙서
작성 방식: draft_attachment
필요 입력값: owner_or_manager_name, owner_or_manager_phone, property_address, applicant_name, business_name, ad_type, display_location, consent_period, consent_date
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 시설사용계약서

```text
template_id: facility_use_agreement
문서명: 시설사용계약서
작성 방식: draft_private_document
필요 입력값: facility_owner, facility_user, facility_address, use_scope, use_period, fee_terms
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 식품 영업 신고서/영업신고 신청서

```text
template_id: food_business_report_application
문서명: 식품 영업 신고서/영업신고 신청서
작성 방식: fill_official_form
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, business_name, business_registration_no, business_address, business_phone, opening_date, business_type, business_area_m2, facility_summary, uses_lpg, is_fire_certificate_target, uses_groundwater, has_children_play_facility, agent_name
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 식품자동판매기의 종류 및 설치장소가 적힌 서류

```text
template_id: vending_machine_installation_list
문서명: 식품자동판매기의 종류 및 설치장소가 적힌 서류
작성 방식: draft_list
필요 입력값: machine_count, machine_types, installation_addresses, serial_or_management_numbers
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 양도양수계약서

```text
template_id: business_transfer_agreement
문서명: 양도양수계약서
작성 방식: draft_private_document
필요 입력값: transferor_name, transferee_name, business_name, business_address, transfer_assets, transfer_price, deposit_terms, succession_date, liability_terms
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 영업자 지위승계신고서

```text
template_id: food_business_succession_report
문서명: 영업자 지위승계신고서
작성 방식: fill_official_form
필요 입력값: transferor_name, transferor_phone, transferee_name, transferee_phone, business_name, business_address, succession_reason, succession_date, license_or_report_no
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 옥외광고물 표시 신청서

```text
template_id: outdoor_ad_display_application
문서명: 옥외광고물 표시 신청서
작성 방식: fill_official_form
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, business_name, business_registration_no, business_address, business_phone, opening_date, ad_type, display_location, ad_width, ad_height, ad_quantity, ad_content, materials, lighting_method, installer_name
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 원색사진 또는 원색도안

```text
template_id: ad_color_design_draft
문서명: 원색사진 또는 원색도안
작성 방식: draft_design_spec
필요 입력값: ad_content, brand_logo_or_text, colors, ad_dimensions, placement_context, reference_image
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 위임장

```text
template_id: power_of_attorney
문서명: 위임장
작성 방식: draft_attachment
필요 입력값: principal_name, principal_id_or_registration_no, principal_address, agent_name, agent_id_or_birth, agent_address, delegated_task, delegation_date
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 위치도

```text
template_id: location_map_description
문서명: 위치도
작성 방식: draft_map_description
필요 입력값: site_address, nearby_landmarks, road_name, occupation_area_m2, north_direction
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 임대차계약서

```text
template_id: lease_agreement_summary
문서명: 임대차계약서
작성 방식: draft_private_document
필요 입력값: lessor_name, lessee_name, property_address, leased_area, deposit, monthly_rent, lease_period, permitted_use, special_terms
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 입간판 도안

```text
template_id: standing_banner_design_spec
문서명: 입간판 도안
작성 방식: draft_design_spec
필요 입력값: banner_width, banner_height, ad_content, colors, placement_photo
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 제조ㆍ가공하려는 식품 및 식품첨가물의 종류 및 제조방법설명서

```text
template_id: food_manufacturing_method_description
문서명: 제조ㆍ가공하려는 식품 및 식품첨가물의 종류 및 제조방법설명서
작성 방식: draft_description
필요 입력값: product_names, ingredients, process_steps, storage_method, packaging_method, shelf_life
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 주요지하매설물의 사후관리계획

```text
template_id: underground_facility_aftercare_plan
문서명: 주요지하매설물의 사후관리계획
작성 방식: draft_description
필요 입력값: facility_type, facility_manager, inspection_plan, restoration_plan, emergency_response
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```

## 통신판매업 신고서

```text
template_id: mail_order_sales_report
문서명: 통신판매업 신고서
작성 방식: fill_official_form
필요 입력값: applicant_name, applicant_birth_or_registration_no, applicant_phone, applicant_address, business_name, business_registration_no, business_address, business_phone, opening_date, online_store_url, hosting_provider, sales_items, sales_method, payment_method, escrow_or_purchase_safety
요청: 위 입력값을 바탕으로 제출용 초안/기입값 JSON을 작성해줘. 비어 있는 값은 [확인 필요]로 남겨줘. 첨부해야 하는 증빙과 제출 전 확인사항도 함께 표시해줘.
```
