from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(Path(__file__).resolve().parents[2] / ".env")


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_env: str
    enable_llm: bool
    enable_graph_rag: bool
    enable_demo_fallback: bool
    llm_provider: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: float
    graph_rag_base_url: str
    graph_rag_api_key: str
    graph_rag_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_env=os.getenv("APP_ENV", "local"),
            enable_llm=_env_bool("ENABLE_LLM", True),
            enable_graph_rag=_env_bool("ENABLE_GRAPH_RAG", False),
            enable_demo_fallback=_env_bool("ENABLE_DEMO_FALLBACK", True),
            llm_provider=os.getenv("LLM_PROVIDER", "openai-compatible"),
            llm_api_key=os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "12")),
            graph_rag_base_url=os.getenv("GRAPH_RAG_BASE_URL", "").rstrip("/"),
            graph_rag_api_key=os.getenv("GRAPH_RAG_API_KEY", ""),
            graph_rag_timeout_seconds=float(os.getenv("GRAPH_RAG_TIMEOUT_SECONDS", "8")),
        )

    @property
    def llm_available(self) -> bool:
        return self.enable_llm and bool(self.llm_api_key)

    @property
    def graph_rag_available(self) -> bool:
        return self.enable_graph_rag and bool(self.graph_rag_base_url)


settings = Settings.from_env()
