from .base import BaseLLM, LLMResult

class MockLLM(BaseLLM):
    def __init__(self, script=None):
        self.script = list(script or [])

    def chat(self, system: str, messages: list, tools: list | None) -> LLMResult:
        if self.script:
            return self.script.pop(0)
        return LLMResult(text='Mock response', tool_calls=[])

