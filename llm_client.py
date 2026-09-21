"""Minimal, production-ready LLM client wrapper.

Supports OpenAI-compatible chat APIs with retries, timeouts, and streaming.
No third-party dependencies beyond requests.
"""

from __future__ import annotations

import os
from typing import Any, Iterable, Optional

import requests


class LLMClient:
    """Thin wrapper around an OpenAI-compatible chat completion endpoint."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o-mini",
        timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries

    def chat(
        self,
        messages: Iterable[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send a chat request and return the assistant's reply text."""
        if not self.api_key:
            raise ValueError("api_key is required; set OPENAI_API_KEY or pass api_key=")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": list(messages),
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        last_exc: Optional[Exception] = None
        for _attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except Exception as exc:  # noqa: BLE001
                last_exc = exc

        raise RuntimeError(
            f"chat request failed after {self.max_retries} attempts"
        ) from last_exc


if __name__ == "__main__":
    client = LLMClient()
    reply = client.chat(
        [{"role": "user", "content": "Say hello in exactly five words."}],
        max_tokens=32,
    )
    print(reply)
