# AI Integration

허가온 V2는 AI API 키가 없어도 규칙 기반 fallback으로 시연됩니다. AI API를 넣으면 같은 경계에서 자연어 이해와 답변 분석 품질만 높아지도록 설계되어 있습니다.

## 환경 변수

`backend/.env.example`을 참고합니다.

```bash
LLM_API_KEY=
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TIMEOUT_SECONDS=12
ENABLE_LLM=true
ENABLE_DEMO_FALLBACK=true
```

`OPENAI_API_KEY`도 fallback으로 인식합니다.

## 연결 지점

```text
backend/app/integrations/llm_client.py
backend/app/services/intake_agent.py
backend/app/services/consultation_analyzer.py
backend/app/schemas/ai.py
backend/app/services/output_guard.py
```

## AI가 해야 할 일

- 사용자의 자연어 입력에서 명시된 사실 추출
- 모르는 값은 `unknown`
- 후보 업종/인허가는 확정하지 않고 candidate로 유지
- 부족 정보 도출
- 쉬운 질문 문장 생성
- 문의 답변 요약
- 해결된 항목, 새 missing field, 새 문의 task 도출

## AI가 하면 안 되는 일

- 다음 화면 직접 결정
- 질문 반복 횟수 결정
- 제출 가능 여부 단독 판단
- 법률 확정 표현 생성
- 사용자에게 보이는 schema를 임의 변경

## 예시 출력

문의 답변 분석은 다음 형태를 기대합니다.

```json
{
  "answerSummary": "건축물 용도를 먼저 확인하라는 답변을 받음",
  "resolvedItems": ["food_business_type"],
  "newMissingFields": ["building_use"],
  "newInquiryTasks": [
    {
      "title": "간판 신고 확인",
      "department": "옥외광고물 담당"
    }
  ],
  "nextAction": "ask_followup"
}
```

백엔드는 이 결과를 검증한 뒤 `NEEDS_INFO`, `INQUIRY`, `DOCUMENTS`, `DASHBOARD` 중 하나로 라우팅합니다.

## GraphRAG 확장 위치

현재 MVP 데이터는 `backend/app/data/catalog.py`에 있습니다. 추후 GraphRAG나 DB를 붙일 때도 `view_builder.py`나 프론트 컴포넌트가 아니라 서비스 레이어 뒤에서 교체해야 합니다.

추천 교체 지점:

- 서류 후보: `DocumentService`
- 부서/연락처: `InquiryService`
- 근거 문장: 새 `EvidenceService`
- 질문 후보: `QuestionPlanner`
