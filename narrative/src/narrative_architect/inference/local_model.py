"""Loopback-only Ollama adapter for skill-bound creative generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class LocalModelError(RuntimeError):
    """Raised when approved local inference is unavailable or invalid."""


@dataclass(frozen=True, slots=True)
class OllamaLocalModel:
    model: str = "qwen2.5:7b-instruct"
    base_url: str = "http://127.0.0.1:11434"
    timeout_seconds: int = 90

    def __post_init__(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise LocalModelError("local inference endpoint must be loopback-only")

    def available(self) -> bool:
        try:
            with urlopen(f"{self.base_url}/api/tags", timeout=1) as response:  # noqa: S310
                return response.status == 200
        except (OSError, URLError):
            return False

    def generate(self, *, skill_markdown: str, context: str, request: str) -> str:
        prompt = (
            "You are a bounded screenplay construction generator. Treat the supplied skill as "
            "the governing craft procedure. Do not silently alter established facts.\n\n"
            f"SKILL\n{skill_markdown}\n\nCANONICAL CONTEXT\n{context}\n\nAUTHOR REQUEST\n{request}"
        )
        body = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode()
        request_obj = Request(  # noqa: S310 - base URL is loopback-validated above
            f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request_obj, timeout=self.timeout_seconds) as response:  # noqa: S310
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, URLError, json.JSONDecodeError) as exc:
            raise LocalModelError("local model generation failed") from exc
        text = payload.get("response")
        if not isinstance(text, str) or not text.strip():
            raise LocalModelError("local model returned no usable text")
        return text.strip()
