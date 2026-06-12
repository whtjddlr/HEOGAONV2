# 허가온 V2

요식업 인허가 준비를 돕는 시연용 MVP입니다. 사용자가 자연어로 준비 상황을 입력하면 백엔드가 정보 수집 루프, 사전 진단, 서류 체크리스트, 문의 답변 반영, 진행 현황, 제출 완료 화면을 순서대로 제어합니다.

## 핵심 원칙

- 프론트는 백엔드가 내려준 `view.type`과 schema만 렌더링합니다.
- 백엔드는 case 상태, 질문 루프, 화면 전환, 무한루프 방지, 서류/문의 진행 상태를 통제합니다.
- AI는 판단과 문안 생성을 맡는 경계로 분리되어 있으며, API 키가 없으면 규칙 기반 fallback으로 시연 가능합니다.
- GraphRAG/문서 DB는 현재 `catalog.py` 상수로 대체되어 있고, 서비스 레이어 뒤에서 교체할 수 있게 설계했습니다.

## 프로젝트 구조

```text
backend/                 FastAPI 상태 머신/API
frontend/                Next.js React 모바일 UI
docs/                    흐름, API, AI 연동 문서
AGENTS.md                Codex/Claude 공통 작업 규칙
CLAUDE.md                Claude Code 빠른 진입 가이드
DESIGN.md                디자인/워딩/모바일 화면 규칙
```

## 실행

```bash
npm run install:all
npm run dev
```

접속 URL:

```text
Frontend: http://127.0.0.1:3100
Backend:  http://127.0.0.1:4100
```

개별 실행:

```bash
cd backend
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 4100

cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3100
```

## 검증

```bash
cd frontend && npm run build
cd .. && python -m compileall backend/app
```

## 주요 문서

- [DESIGN.md](./DESIGN.md): 허가온 모바일 UI, 문구, 진행바, 대시보드, 완료 화면 기준
- [AGENTS.md](./AGENTS.md): 에이전트가 코딩할 때 지켜야 할 구조, 금지사항, 검증 절차
- [CLAUDE.md](./CLAUDE.md): Claude Code용 빠른 작업 가이드
- [docs/flow-contract.md](./docs/flow-contract.md): 상태 머신과 화면 흐름 계약
- [docs/api-contract.md](./docs/api-contract.md): 프론트-백엔드 API schema
- [docs/ai-integration.md](./docs/ai-integration.md): AI API만 연결하면 동작하도록 둔 경계
- [docs/demo-script.md](./docs/demo-script.md): 시연 흐름

## MVP 상태 머신

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

`REVISION`은 MVP 부담을 줄이기 위해 제외했습니다. 보완/반려 루프는 추후 제출 후 상태 관리로 확장합니다.
