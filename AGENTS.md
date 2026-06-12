# 에이전트 작업 가이드

Claude Code, Codex, 다른 코딩 에이전트가 이 저장소를 수정할 때 따를 규칙입니다.

## 절대 원칙

- 프론트가 흐름을 판단하지 않습니다.
- 백엔드가 현재 단계와 다음 화면을 결정합니다.
- AI 응답은 항상 백엔드에서 검증하고 프론트 schema로 변환합니다.
- 서류, 문의, 질문 반복 제한은 백엔드 책임입니다.
- MVP에서 반려/보완 루프는 제외되어 있습니다.

## 역할 분리

### Frontend

- `view.type`에 맞는 화면 렌더링
- 사용자 입력/선택 수집
- 진행 상태 표시
- 체크박스, 탭, 버튼, 모달 같은 UI 상태 처리
- 백엔드가 준 `nextButtonLabel`, `sections`, `documents`, `inquiryTasks` 사용

프론트에서 하지 말 것:

- 다음 질문 직접 선택
- 서류 필요 여부 판단
- 제출 가능 여부 임의 판단
- AI 응답 원문 직접 신뢰
- 상태 머신 임의 구현

### Backend

- case 생성 및 상태 저장
- 상태 머신 전환
- 질문 루프 제어
- field별 최대 질문 횟수 제한
- 전체 질문 수 제한
- `unknown/skipped` 처리
- 사전 진단 결과 생성
- 서류 우선순위 정렬
- 문의 task 생성
- 문의 답변 분석 결과 반영
- AI/GraphRAG 결과 검증

### AI / GraphRAG

- 자연어 입력에서 명시 사실 추출
- 부족 정보 도출
- 쉬운 질문 생성
- 서류/부서/근거 확장
- 문의 답변 요약과 resolved/missing/task 판단

현재 MVP는 API 키 없이도 동작하도록 규칙 기반 fallback을 둡니다.

## 주요 파일

```text
frontend/src/components/HeogaonFlowApp.tsx      앱 상태와 API 호출 연결
frontend/src/components/views/FlowView.tsx      view.type 라우팅
frontend/src/components/views/*                 화면별 UI
frontend/src/components/shell/*                 헤더, 하단바, 진행 현황
frontend/src/types/flow.ts                      프론트 API 타입 계약
frontend/app/styles/*.css                       디자인 시스템과 화면 스타일

backend/app/services/flow_service.py            상태 머신
backend/app/services/question_planner.py        정보 수집 루프
backend/app/services/view_builder.py            프론트 view schema 생성
backend/app/services/document_service.py        서류 생성/완료 처리
backend/app/services/inquiry_service.py         문의 task/문안
backend/app/services/consultation_analyzer.py   문의 답변 분석
backend/app/integrations/llm_client.py          AI API 경계
backend/app/data/catalog.py                     MVP 데이터/질문/서류 seed
```

## 상태 머신

```text
INTAKE -> UNDERSTAND -> NEEDS_INFO -> DIAGNOSIS -> DOCUMENTS
DOCUMENTS -> INQUIRY | DASHBOARD
INQUIRY -> ANSWER_REVIEW
ANSWER_REVIEW -> NEEDS_INFO | INQUIRY | DOCUMENTS | DASHBOARD
DASHBOARD -> DOCUMENTS | INQUIRY | SUBMITTED
```

`SUBMITTED`는 모든 서류 완료와 열린 문의 없음 조건을 만족할 때만 진입합니다.

## API 계약

프론트는 항상 다음 형태를 받습니다.

```ts
{
  ok: boolean;
  caseId: string;
  view: ApiView;
  caseState: {
    status: string;
    currentStep: string;
    progressStage: string;
  };
  statePatch: {
    slots: Record<string, SlotRecord>;
    answers: AnswerLog[];
    documents: DocumentItem[];
    inquiryTasks: InquiryTask[];
    completedDocumentIds: string[];
    questionLoop: QuestionLoop;
  };
}
```

새 화면을 추가할 때는 `frontend/src/types/flow.ts`, `backend/app/services/view_builder.py`, `frontend/src/components/views/FlowView.tsx`를 함께 수정합니다.

## 디자인 수정 규칙

- 먼저 [DESIGN.md](./DESIGN.md)를 읽습니다.
- 로고는 `BrandLogo`만 수정합니다.
- 본문 폰트 변경으로 로고가 깨지지 않게 합니다.
- 모바일 기준으로 확인합니다.
- 카드 안에 카드 중첩을 만들지 않습니다.
- 버튼 문구는 짧은 행동으로 씁니다.
- 하단 고정 버튼과 스크롤 콘텐츠가 겹치지 않게 합니다.

## 검증 명령

```bash
cd frontend && npm run build
cd .. && python -m compileall backend/app
```

흐름 검증은 최소한 다음을 확인합니다.

- 자연어 입력 후 로딩 화면이 나온다.
- 정보 수집 질문이 한 번에 하나씩 나온다.
- `아직 몰라요` 선택 시 다음 질문으로 넘어간다.
- 진단 후 서류 화면으로 간다.
- 모든 서류를 체크해야 다음으로 간다.
- 문의 답변 저장 후 대시보드로 돌아온다.
- 모든 서류와 문의가 끝난 뒤에만 제출 완료 화면으로 간다.

## AI API 연결 시 주의

- `.env`에 `LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`을 넣습니다.
- AI 응답은 `backend/app/schemas/ai.py` schema를 통과해야 합니다.
- AI가 확정 표현을 내도 프론트에는 후보/확인 필요 형태로 내려야 합니다.
- 법률 자문처럼 보이는 확정 문구는 `output_guard.py`에서 완화합니다.

## 커밋 전 체크

- `node_modules`, `.next`, `.venv`, `__pycache__`, `.env`는 커밋하지 않습니다.
- 기존 사용자 변경을 되돌리지 않습니다.
- 구조 변경 시 문서도 함께 업데이트합니다.
- 백엔드 계약을 바꾸면 프론트 타입과 docs도 같이 수정합니다.
