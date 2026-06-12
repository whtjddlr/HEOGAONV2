from __future__ import annotations

from typing import Any


class InMemoryCaseRepository:
    def __init__(self) -> None:
        self.cases: dict[str, dict[str, Any]] = {}

    def add(self, case: dict[str, Any]) -> dict[str, Any]:
        self.cases[case["caseId"]] = case
        return case

    def get(self, case_id: str) -> dict[str, Any] | None:
        return self.cases.get(case_id)

    def exists(self, case_id: str) -> bool:
        return case_id in self.cases


case_repository = InMemoryCaseRepository()
