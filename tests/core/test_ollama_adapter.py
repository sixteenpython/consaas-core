import json

import pytest

from core.ai.adapters.ollama import OllamaProvider
from core.ai.contracts import GenerationRequest


def test_adapter_rejects_remote_endpoint() -> None:
    with pytest.raises(ValueError, match="loopback-local"):
        OllamaProvider("https://example.com")


def test_adapter_sends_structured_local_request() -> None:
    captured: dict[str, object] = {}

    def transport(request: object, timeout: float) -> bytes:
        captured["request"] = request
        captured["timeout"] = timeout
        return json.dumps({"response": '{"premise":"A choice"}'}).encode()

    provider = OllamaProvider(transport=transport)
    result = provider.generate(
        GenerationRequest(
            task="extract",
            system_prompt="Return JSON",
            user_prompt="A story",
            response_schema={"type": "object"},
        ),
        model_id="granite3.3:8b",
    )

    assert result.provider == "ollama"
    assert result.text == '{"premise":"A choice"}'
    assert captured["timeout"] == 120.0
