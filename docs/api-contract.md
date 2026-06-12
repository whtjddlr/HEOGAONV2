# API Contract

기본 API 주소는 `http://127.0.0.1:4100`입니다.

## Create Case

```http
POST /api/cases
Content-Type: application/json
```

```json
{
  "input": {
    "type": "natural_language",
    "text": "연남동에서 디저트 카페를 열고 싶어요"
  }
}
```

## Apply Turn

```http
POST /api/cases/{caseId}/turns
Content-Type: application/json
```

질문 답변:

```json
{
  "input": {
    "type": "slot_answer",
    "fieldKey": "on_site_consumption",
    "optionIds": ["yes"],
    "unknown": false
  }
}
```

모름 처리:

```json
{
  "input": {
    "type": "slot_answer",
    "fieldKey": "building_use",
    "optionIds": ["unknown"],
    "unknown": true
  }
}
```

명시 액션:

```json
{
  "input": {
    "type": "action",
    "actionId": "documents"
  }
}
```

서류 체크:

```json
{
  "input": {
    "type": "document_toggle",
    "documentId": "building_register",
    "completed": true
  }
}
```

문의 채널:

```json
{
  "input": {
    "type": "inquiry_channel",
    "channel": "online"
  }
}
```

문의 답변:

```json
{
  "input": {
    "type": "consultation_answer",
    "text": "건축물 용도를 먼저 확인하라는 답변을 받았습니다."
  }
}
```

## Envelope

모든 응답은 같은 envelope 형태입니다.

```json
{
  "ok": true,
  "caseId": "case_xxx",
  "turnId": "turn_1",
  "view": {
    "type": "slot_question"
  },
  "caseState": {
    "status": "NEEDS_INFO",
    "currentStep": "slot_question",
    "progressStage": "intake"
  },
  "statePatch": {
    "slots": {},
    "answers": [],
    "documents": [],
    "inquiryTasks": [],
    "completedDocumentIds": [],
    "questionLoop": {}
  },
  "meta": {
    "schemaVersion": "flow-v2",
    "source": "rules+ai-boundary",
    "fallback": true,
    "warnings": []
  }
}
```

정확한 TypeScript 타입은 `frontend/src/types/flow.ts`를 기준으로 합니다.
