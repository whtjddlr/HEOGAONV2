from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from app.core.config import Settings, settings
from app.services.output_guard import clean_payload, mask_sensitive_text


class LlmClient:
    """OpenAI-compatible JSON client.

    The rest of the backend depends on this small boundary only. Set
    LLM_API_KEY and LLM_MODEL to enable AI; leave them empty to use rule fallback.
    """

    def __init__(self, config: Settings = settings) -> None:
        self.config = config

    @property
    def available(self) -> bool:
        return self.config.llm_available

    def generate_json(self, *, system_prompt: str, user_payload: dict[str, Any]) -> dict[str, Any] | None:
        if not self.available:
            return None

        payload = {
            "model": self.config.llm_model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(clean_payload(user_payload), ensure_ascii=False),
                },
            ],
        }
        request = urllib.request.Request(
            f"{self.config.llm_base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.config.llm_api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.llm_timeout_seconds) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
            return None

        content = raw.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            return None

        try:
            parsed = json.loads(mask_sensitive_text(content))
        except json.JSONDecodeError:
            return None
        return clean_payload(parsed)


llm_client = LlmClient()
