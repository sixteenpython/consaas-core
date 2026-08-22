"""Minimal local-only Ollama adapter using the Python standard library."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from collections.abc import Callable
from typing import cast
from urllib.parse import urlparse

from core.ai.contracts import GenerationRequest, GenerationResult

Transport = Callable[[urllib.request.Request, float], bytes]


def _default_transport(request: urllib.request.Request, timeout: float) -> bytes:
    # The constructor below admits only HTTP on a loopback host.
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
        return cast(bytes, response.read())


class OllamaProvider:
    """Call an Ollama daemon and reject non-local endpoints by construction."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        *,
        timeout_seconds: float = 120.0,
        transport: Transport = _default_transport,
    ) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("Ollama endpoint must use HTTP on a loopback-local host")
        self._url = f"{base_url.rstrip('/')}/api/generate"
        self._timeout = timeout_seconds
        self._transport = transport

    def generate(self, request: GenerationRequest, *, model_id: str) -> GenerationResult:
        prompt = f"SYSTEM:\n{request.system_prompt}\n\nUSER:\n{request.user_prompt}"
        payload: dict[str, object] = {
            "model": model_id,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": request.temperature},
        }
        if request.response_schema is not None:
            payload["format"] = request.response_schema
        body = json.dumps(payload, separators=(",", ":")).encode()
        http_request = urllib.request.Request(
            self._url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        started = time.perf_counter()
        raw = self._transport(http_request, self._timeout)
        latency_ms = round((time.perf_counter() - started) * 1000)
        decoded = json.loads(raw)
        if not isinstance(decoded.get("response"), str):
            raise ValueError("Ollama response did not contain text")
        return GenerationResult(
            text=decoded["response"],
            model_id=model_id,
            provider="ollama",
            latency_ms=latency_ms,
            prompt_hash=hashlib.sha256(prompt.encode()).hexdigest(),
        )
