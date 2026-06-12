from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_env: str
    enable_llm: bool
    enable_demo_fallback: bool
    llm_provider: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_env=os.getenv("APP_ENV", "local"),
            enable_llm=_env_bool("ENABLE_LLM", True),
            enable_demo_fallback=_env_bool("ENABLE_DEMO_FALLBACK", True),
            llm_provider=os.getenv("LLM_PROVIDER", "openai-compatible"),
            llm_api_key=os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "12")),
        )

    @property
    def llm_available(self) -> bool:
        return self.enable_llm and bool(self.llm_api_key)


settings = Settings.from_env()
