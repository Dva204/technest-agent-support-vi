import pytest
from app.db import reset_db, snapshot
from app.agent.session import Session
from app.agent.tools import (
    call,
    SearchIn,
    StockIn,
    OrderIn,
    ShipIn,
    ShipItem,
    PrepareReturnIn,
    CommitIn,
    EscalateIn,
    prepare_return,
    commit_return,
    decide_return
)

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    monkeypatch.setenv('SHOP_NOW', '2026-11-10')
    reset_db()

def test_search_products():
    s = Session(id='t')
    res = call('search_products', {'query': 'Aurora'}, s, {})
    assert res['ok'] is True
    ids = [item['id'] for item in res['items']]
    assert 'P01' in ids

def test_check_stock():
    s = Session(id='t')
    res = call('check_stock', {'product_id': 'P01'}, s, {})
    assert res['ok'] is True
    assert len(res['variants']) == 2

    res_nf = call('check_stock', {'product_id': 'P999'}, s, {})
    assert res_nf['ok'] is False
    assert res_nf['code'] == 'ERR_NOT_FOUND'

def test_order_auth_check():
    s = Session(id='t')
    # Đúng số điện thoại
    res_ok = call('get_order_status', {'order_id': 'TN-1001', 'phone': '0900000001'}, s, {})
    assert res_ok['ok'] is True
    assert res_ok['status'] == 'delivered'

    # Sai số điện thoại
    res_err = call('get_order_status', {'order_id': 'TN-1001', 'phone': '0900000002'}, s, {})
    assert res_err['ok'] is False
    assert res_err['code'] == 'ERR_AUTH'

def test_calc_shipping_fee():
    s = Session(id='t')
    # Đơn dưới 1 triệu: Hà Nội 20k, TP.HCM 20k, Đà Nẵng 30k, Cần Thơ 40k
    res_hn = call('calc_shipping_fee', {'city': 'Hà Nội', 'items': [{'product_id': 'P02', 'qty': 1}]}, s, {})
    assert res_hn['fee'] == 20000

    res_hcm = call('calc_shipping_fee', {'city': 'TP. Hồ Chí Minh', 'items': [{'product_id': 'P02', 'qty': 1}]}, s, {})
    assert res_hcm['fee'] == 20000

    res_dn = call('calc_shipping_fee', {'city': 'Đà Nẵng', 'items': [{'product_id': 'P02', 'qty': 1}]}, s, {})
    assert res_dn['fee'] == 30000

    res_ct = call('calc_shipping_fee', {'city': 'Cần Thơ', 'items': [{'product_id': 'P05', 'qty': 1}]}, s, {})
    assert res_ct['fee'] == 40000

    # Đơn trên 1 triệu: Miễn phí (0đ)
    res_free = call('calc_shipping_fee', {'city': 'Hà Nội', 'items': [{'product_id': 'P01', 'qty': 1}]}, s, {})
    assert res_free['fee'] == 0

def test_return_policy_expired_7d():
    s = Session(id='t')
    # TN-1002 giao ngày 2026-10-29 (12 ngày trước) -> Quá hạn 7 ngày đổi ý
    a = PrepareReturnIn(order_id='TN-1002', phone='0900000001', product_id='P01', reason='change_mind')
    res = prepare_return(a, s, {'policy_engine': True})
    assert res['ok'] is False
    assert res['code'] == 'ERR_EXPIRED_7D'

def test_return_policy_activated():
    s = Session(id='t')
    # TN-1003 đã kích hoạt (activated=1) -> Không đổi ý
    a = PrepareReturnIn(order_id='TN-1003', phone='0900000002', product_id='P01', reason='change_mind')
    res = prepare_return(a, s, {'policy_engine': True})
    assert res['ok'] is False
    assert res['code'] == 'ERR_ACTIVATED'

def test_return_policy_opened_earbuds():
    s = Session(id='t')
    # TN-1007 tai nghe đã mở hộp (opened=1) -> Từ chối vệ sinh
    a = PrepareReturnIn(order_id='TN-1007', phone='0900000004', product_id='P02', reason='change_mind')
    res = prepare_return(a, s, {'policy_engine': True})
    assert res['ok'] is False
    assert res['code'] == 'ERR_OPENED_HYGIENE'

def test_return_policy_valid_defect():
    s = Session(id='t')
    # TN-1001 lỗi trong 30 ngày -> Hợp lệ
    a = PrepareReturnIn(order_id='TN-1001', phone='0900000001', product_id='P02', reason='defect')
    res = prepare_return(a, s, {'policy_engine': True})
    assert res['ok'] is True
    assert res['code'] == 'OK_DEFECT'
    assert 'token' in res

def test_enforce_confirm_guard():
    s = Session(id='t')
    prep = call('prepare_return', {'order_id': 'TN-1001', 'phone': '0900000001', 'product_id': 'P02', 'reason': 'defect'}, s, {'policy_engine': True})
    token = prep['token']

    # Khi khách chưa xác nhận: Guard chặn
    s.last_user_confirmed = False
    commit_fail = call('commit_return', {'token': token}, s, {'enforce_confirm': True})
    assert commit_fail['ok'] is False
    assert commit_fail['code'] == 'ERR_NEED_CONFIRM'
    assert len(snapshot()['returns']) == 0

    # Khi khách đã xác nhận: Guard cho phép ghi CSDL
    s.last_user_confirmed = True
    commit_ok = call('commit_return', {'token': token}, s, {'enforce_confirm': True})
    assert commit_ok['ok'] is True
    assert len(snapshot()['returns']) == 1

def test_escalate_to_human():
    s = Session(id='t')
    res = call('escalate_to_human', {'reason': 'complaint', 'summary': 'Giao hàng chậm'}, s, {})
    assert res['ok'] is True
    snap = snapshot()
    assert len(snap['escalations']) == 1
    assert snap['escalations'][0]['session_id'] == 't'

