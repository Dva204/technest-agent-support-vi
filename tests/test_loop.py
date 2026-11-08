import pytest
from app.db import reset_db, snapshot
from app.agent.session import Session
from app.agent.loop import run_turn
from app.agent.llm import MockLLM, LLMResult

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    monkeypatch.setenv('SHOP_NOW', '2026-11-10')
    reset_db()

def test_read_only_turn():
    s = Session(id='t1')
    cfg = {'tools_enabled': True, 'policy_engine': True, 'enforce_confirm': True}
    
    # Giả lập: lượt 1 LLM gọi get_order_status, lượt 2 LLM trả lời kết quả
    script = [
        LLMResult(
            text='',
            tool_calls=[{'id': 'c1', 'name': 'get_order_status', 'input': {'order_id': 'TN-1001', 'phone': '0900000001'}}],
            raw_content='call_status'
        ),
        LLMResult(
            text='Đơn hàng TN-1001 của bạn đã được giao vào ngày 2026-11-07.',
            tool_calls=[],
            raw_content='final_reply'
        )
    ]
    llm = MockLLM(script)
    reply = run_turn(s, 'Tôi là 0900000001, đơn TN-1001 sao rồi?', llm, cfg)
    assert '2026-11-07' in reply
    assert len(s.log) == 1
    assert s.log[0]['name'] == 'get_order_status'

def test_multi_turn_return_flow():
    s = Session(id='t2')
    cfg = {'tools_enabled': True, 'policy_engine': True, 'enforce_confirm': True}

    class MockDialogLLM:
        def __init__(self, session):
            self.session = session
            self.step = 0

        def chat(self, system, messages, tools):
            self.step += 1
            if self.step == 1:
                return LLMResult(
                    text='',
                    tool_calls=[{
                        'id': 'call_p',
                        'name': 'prepare_return',
                        'input': {'order_id': 'TN-1001', 'phone': '0900000001', 'product_id': 'P02', 'reason': 'defect'}
                    }],
                    raw_content='prepare'
                )
            elif self.step == 2:
                return LLMResult(
                    text='Tôi đã chuẩn bị yêu cầu đổi tai nghe Nova Buds 2. Bạn xác nhận nhé?',
                    tool_calls=[],
                    raw_content='ask_confirm'
                )
            elif self.step == 3:
                token = list(self.session.pending.keys())[0]
                return LLMResult(
                    text='',
                    tool_calls=[{'id': 'call_c', 'name': 'commit_return', 'input': {'token': token}}],
                    raw_content='commit'
                )
            else:
                return LLMResult(
                    text='Đã tạo yêu cầu đổi hàng thành công!',
                    tool_calls=[],
                    raw_content='finish'
                )

    llm = MockDialogLLM(s)
    # Lượt 1: Yêu cầu đổi trả
    reply1 = run_turn(s, 'Tôi là 0900000001. Tai nghe đơn TN-1001 bị rè, muốn đổi.', llm, cfg)
    assert 'xác nhận' in reply1.lower()
    assert len(snapshot()['returns']) == 0

    # Lượt 2: Xác nhận
    reply2 = run_turn(s, 'Đúng rồi, xác nhận giúp tôi.', llm, cfg)
    assert 'thành công' in reply2.lower()
    assert len(snapshot()['returns']) == 1

