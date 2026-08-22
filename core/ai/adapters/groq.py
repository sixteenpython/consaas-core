"""Optional hosted-demo Groq adapter using only the Python standard library."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any, cast

from core.ai.contracts import GenerationRequest, GenerationResult

Transport = Callable[[urllib.request.Request, float], bytes]


def _default_transport(request: urllib.request.Request, timeout: float) -> bytes:
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
        return cast(bytes, response.read())


class GroqProvider:
    """Call the fixed Groq endpoint; product logic remains provider-neutral."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout_seconds: float = 45.0,
        transport: Transport = _default_transport,
    ) -> None:
        if not api_key.strip():
            raise ValueError("Groq API key is required")
        self._api_key = api_key.strip()
        self._timeout = timeout_seconds
        self._transport = transport
        self._url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, request: GenerationRequest, *, model_id: str) -> GenerationResult:
        prompt = f"SYSTEM:\n{request.system_prompt}\n\nUSER:\n{request.user_prompt}"
        payload: dict[str, Any] = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "temperature": request.temperature,
            "max_completion_tokens": 900,
        }
        if request.response_schema is not None:
            payload["response_format"] = {"type": "json_object"}
        http_request = urllib.request.Request(
            self._url,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        started = time.perf_counter()
        try:
            raw = self._transport(http_request, self._timeout)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Hosted model returned HTTP {exc.code}") from exc
        decoded = json.loads(raw)
        text = decoded.get("choices", [{}])[0].get("message", {}).get("content")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("hosted model response did not contain text")
        return GenerationResult(
            text=text,
            model_id=model_id,
            provider="groq",
            latency_ms=round((time.perf_counter() - started) * 1000),
            prompt_hash=hashlib.sha256(prompt.encode()).hexdigest(),
        )
