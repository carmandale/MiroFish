from app.utils.llm_client import LLMClient


class FakeCompletions:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)

        class Message:
            content = '{"ok": true}'

        class Choice:
            message = Message()

        class Response:
            choices = [Choice()]

        return Response()


class FakeChat:
    def __init__(self, completions):
        self.completions = completions


class FakeOpenAIClient:
    def __init__(self):
        self.completions = FakeCompletions()
        self.chat = FakeChat(self.completions)


def _build_client(model: str) -> tuple[LLMClient, FakeCompletions]:
    client = LLMClient(api_key="test-key", model=model)
    fake_client = FakeOpenAIClient()
    client.client = fake_client
    return client, fake_client.completions


def test_chat_uses_max_completion_tokens_for_gpt5_models():
    client, completions = _build_client("gpt-5-mini")

    client.chat(messages=[{"role": "user", "content": "hello"}], max_tokens=321, temperature=0.2)

    assert completions.calls
    kwargs = completions.calls[0]
    assert kwargs["max_completion_tokens"] == 321
    assert "max_tokens" not in kwargs
    assert "temperature" not in kwargs


def test_chat_uses_max_tokens_for_legacy_models():
    client, completions = _build_client("gpt-4.1")

    client.chat(messages=[{"role": "user", "content": "hello"}], max_tokens=654)

    assert completions.calls
    kwargs = completions.calls[0]
    assert kwargs["max_tokens"] == 654
    assert "max_completion_tokens" not in kwargs
