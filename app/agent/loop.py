import json
from app.agent import tools as T
from app.agent.confirm import is_confirmation
from app.agent.prompts import SYSTEM, SYSTEM_A0

MAX_STEPS = 6
FALLBACK = 'Xin lỗi, tôi chưa xử lý được yêu cầu này. Tôi sẽ chuyển cho nhân viên hỗ trợ.'

def run_turn(s, user_text, llm, cfg):
    s.last_user_confirmed = is_confirmation(user_text)
    s.last_turn_calls = []
    s.messages.append({'role': 'user', 'content': user_text})
    tools_enabled = cfg.get('tools_enabled', True)
    tools = T.schemas() if tools_enabled else []
    system_prompt = SYSTEM if tools_enabled else SYSTEM_A0
    for _ in range(MAX_STEPS):
        r = llm.chat(system_prompt, s.messages, tools)
        s.messages.append({'role': 'assistant', 'content': r.raw_content})
        if not r.tool_calls:
            s.last_reply = r.text
            return r.text
        results = []
        for c in r.tool_calls:
            out = T.call(c['name'], c['input'], s, cfg)
            results.append({
                'type': 'tool_result',
                'tool_use_id': c['id'],
                'name': c['name'],
                'content': json.dumps(out, ensure_ascii=False)
            })
        s.messages.append({'role': 'user', 'content': results})
    s.last_reply = FALLBACK
    return FALLBACK
