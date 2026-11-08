import os
from .base import BaseLLM, LLMResult

class ClaudeLLM(BaseLLM):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        import anthropic
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else anthropic.Anthropic()
        self.model = model or os.environ.get('CLAUDE_MODEL') or os.environ.get('LLM_MODEL', 'claude-3-5-haiku-20241022')
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', 0))
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', 1024))

    def chat(self, system: str, messages: list, tools: list | None) -> LLMResult:
        kwargs = {
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'system': system,
            'messages': messages,
        }
        if tools:
            kwargs['tools'] = tools

        r = self.client.messages.create(**kwargs)
        text = ''.join(b.text for b in r.content if b.type == 'text')
        calls = [{'id': b.id, 'name': b.name, 'input': b.input} for b in r.content if b.type == 'tool_use']
        in_tok = getattr(r.usage, 'input_tokens', 0)
        out_tok = getattr(r.usage, 'output_tokens', 0)
        return LLMResult(text, calls, r.content, in_tok, out_tok)

