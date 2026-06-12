# Flow Contract

허가온 V2의 흐름 계약입니다. 프론트는 이 계약을 해석해서 화면을 그릴 뿐, 다음 단계를 직접 판단하지 않습니다.

## 상태 목록

```text
INTAKE
UNDERSTAND
NEEDS_INFO
DIAGNOSIS
DOCUMENTS
INQUIRY
ANSWER_REVIEW
DASHBOARD
SUBMITTED
```

## 기본 흐름

```text
사용자 자연어 입력
-> case 생성
-> 명시 사실 추출
-> 부족 정보 질문
-> 사전 진단
-> 서류 체크리스트
-> 문의 방법 선택
-> 문의 답변 반영
-> 진행 현황
-> 제출 완료
```

## 질문 루프

백엔드가 담당합니다.

- 질문은 한 번에 하나만 내려줍니다.
- field별 최대 질문 횟수를 제한합니다.
- 전체 질문 수를 제한합니다.
- 사용자가 모르면 `unknown/skipped`로 처리하고 다음 질문으로 이동합니다.
- AI가 같은 field를 반복 요청해도 백엔드가 차단해야 합니다.

## 화면 전환

### `NEEDS_INFO`

`slot_question` view를 반환합니다. 프론트는 input mode에 맞춰 form만 렌더링합니다.

### `DIAGNOSIS`

`diagnosis` view를 반환합니다. 이 화면은 질문 화면이 아니라 판단 결과 요약입니다.

### `DOCUMENTS`

`documents` view를 반환합니다. 모든 서류가 체크되어야 다음 단계 버튼이 활성화됩니다.

### `INQUIRY`

`inquiry` view를 반환합니다. 문의 채널은 `phone`, `online`, `visit`입니다.

### `ANSWER_REVIEW`

문의 답변 분석 결과를 보여주고, 다음 action에서 백엔드가 재라우팅합니다.

### `DASHBOARD`

남은 일, 새로 생긴 일, 업데이트된 일을 보여줍니다. 각 할 일 card는 백엔드 `actionId`를 호출할 수 있습니다.

### `SUBMITTED`

모든 서류 완료와 열린 문의 없음 조건을 만족할 때만 진입합니다.

## 명시 액션

```text
primary
restart
documents
inquiry
dashboard
submitted
```

대시보드와 진행 현황 패널은 `documents`, `inquiry`, `submitted` 같은 명시 액션을 호출합니다. 프론트가 직접 상태를 바꾸지 않습니다.
