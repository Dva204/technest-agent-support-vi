import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from app.db import reset_db, snapshot, diff
from app.agent.session import Session
from app.agent.loop import run_turn
from app.agent.llm import build_llm

app = FastAPI(title="TechNest Agent API")
SESSIONS = {}
CFG = {'tools_enabled': True, 'policy_engine': True, 'enforce_confirm': True}
_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = build_llm()
    return _llm

class ChatIn(BaseModel):
    session_id: str
    message: str

@app.post('/reset')
def reset():
    reset_db()
    SESSIONS.clear()
    return {'ok': True}

@app.post('/chat')
def chat(body: ChatIn):
    s = SESSIONS.setdefault(body.session_id, Session(id=body.session_id))
    before = snapshot()
    reply = run_turn(s, body.message, get_llm(), CFG)
    return {
        'reply': reply,
        'tool_calls': s.last_turn_calls,
        'db_changes': diff(before, snapshot())
    }
