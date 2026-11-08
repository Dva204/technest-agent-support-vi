import os
import json
from .base import BaseLLM, LLMResult

class OpenAICompatLLM(BaseLLM):
    def __init__(self, base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        from openai import OpenAI
        self.base_url = base_url or os.environ.get('OPENAI_BASE_URL') or os.environ.get('OPENAI_API_BASE')
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY', 'dummy-key')
        self.model = model or os.environ.get('OPENAI_MODEL') or os.environ.get('LLM_MODEL', 'gpt-4o-mini')
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', 0))
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', 1024))
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def chat(self, system: str, messages: list, tools: list | None) -> LLMResult:
        # Chuyển đổi tin nhắn nội bộ sang định dạng OpenAI Chat
        oai_messages = [{'role': 'system', 'content': system}]
        for m in messages:
            role = m['role']
            content = m['content']
            if isinstance(content, str):
                oai_messages.append({'role': role, 'content': content})
            elif isinstance(content, list):
                # Kiểm tra định dạng tool_result
                if any(isinstance(c, dict) and c.get('type') == 'tool_result' for c in content):
                    for tr in content:
                        oai_messages.append({
                            'role': 'tool',
                            'tool_call_id': tr.get('tool_use_id'),
                            'content': tr.get('content', '')
                        })
                else:
                    oai_messages.append({'role': role, 'content': str(content)})
            else:
                oai_messages.append({'role': role, 'content': str(content)})

        oai_tools = None
        if tools:
            oai_tools = [{
                'type': 'function',
                'function': {
                    'name': t['name'],
                    'description': t.get('description', ''),
                    'parameters': t.get('input_schema', {})
                }
            } for t in tools]

        kwargs = {
            'model': self.model,
            'messages': oai_messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
        }
        if oai_tools:
            kwargs['tools'] = oai_tools

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        msg = choice.message
        text = msg.content or ''
        calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                fn_args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
                calls.append({
                    'id': tc.id,
                    'name': tc.function.name,
                    'input': fn_args
                })

        usage = getattr(response, 'usage', None)
        in_tok = usage.prompt_tokens if usage else 0
        out_tok = usage.completion_tokens if usage else 0
        return LLMResult(text, calls, msg, in_tok, out_tok)

