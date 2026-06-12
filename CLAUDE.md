# Claude Code Guide

이 저장소는 허가온 V2 MVP입니다. Claude Code가 작업할 때는 이 파일을 먼저 읽고, 더 자세한 규칙은 [AGENTS.md](./AGENTS.md)와 [DESIGN.md](./DESIGN.md)를 따르세요.

## 빠른 실행

```bash
npm run install:all
npm run dev
```

```text
Frontend: http://127.0.0.1:3100
Backend:  http://127.0.0.1:4100
```

## 빠른 검증

```bash
cd frontend && npm run build
cd .. && python -m compileall backend/app
```

## 작업 원칙

- 프론트는 화면만 그립니다.
- 백엔드는 흐름을 통제합니다.
- AI는 판단/질문/요약을 보조하지만, 백엔드가 검증합니다.
- GraphRAG는 서류/부서/근거/질문 후보만 확장하고, 흐름 제어는 백엔드에 둡니다.
- 사용자가 보는 화면에 내부 용어를 노출하지 않습니다.
- MVP에 반려/보완 루프를 다시 넣지 않습니다.

## 자주 수정하는 위치

- 화면 추가/수정: `frontend/src/components/views`
- 앱 흐름 연결: `frontend/src/components/HeogaonFlowApp.tsx`
- API 타입: `frontend/src/types/flow.ts`
- 디자인: `frontend/app/styles`
- 상태 머신: `backend/app/services/flow_service.py`
- 질문 루프: `backend/app/services/question_planner.py`
- 프론트 view schema: `backend/app/services/view_builder.py`
- AI 연결: `backend/app/integrations/llm_client.py`
- GraphRAG 연결: `backend/app/services/graph_rag_service.py`

## 디자인 주의

- 로고는 `BrandLogo` 컴포넌트에서만 관리합니다.
- 모바일 세로 화면에서 먼저 확인합니다.
- 하단 고정 버튼이 콘텐츠를 가리면 화면별 padding을 조정합니다.
- 문구는 짧게 씁니다.

## 백엔드 주의

- 새 흐름은 `actionId` 또는 `machineState` 전환으로 명시합니다.
- 프론트가 다음 단계를 추론하게 만들지 않습니다.
- 모든 서류와 열린 문의가 끝나기 전에는 `SUBMITTED`로 보내지 않습니다.
- GraphRAG는 `POST /retrieve` 계약만 맞추고, 실패 시 catalog fallback이 유지되어야 합니다.

## 문서 업데이트 기준

코드 변경이 다음 중 하나에 해당하면 문서도 같이 수정하세요.

- 새 화면 추가
- API schema 변경
- 상태 머신 변경
- 디자인/문구 기준 변경
- AI 입출력 계약 변경
- GraphRAG 입출력 계약 변경
