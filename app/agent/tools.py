import os
import uuid
from datetime import datetime
from pydantic import BaseModel
from rapidfuzz import process, fuzz
from app.db import conn
from app.agent.confirm import strip_accents

def now():
    return datetime.fromisoformat(os.environ.get('SHOP_NOW', '2026-11-10'))

def days_since(s):
    return (now() - datetime.fromisoformat(s)).days

def norm_phone(p):
    p = ''.join(ch for ch in str(p) if ch.isdigit())
    return '0' + p[2:] if p.startswith('84') else p

class SearchIn(BaseModel):
    query: str

class StockIn(BaseModel):
    product_id: str

class OrderIn(BaseModel):
    order_id: str
    phone: str

class ShipItem(BaseModel):
    product_id: str
    qty: int = 1

class ShipIn(BaseModel):
    city: str
    items: list[ShipItem]

class PrepareReturnIn(BaseModel):
    order_id: str
    phone: str
    product_id: str
    reason: str   # defect hoặc change_mind

class CommitIn(BaseModel):
    token: str

class EscalateIn(BaseModel):
    reason: str
    summary: str

def search_products(a, s, cfg):
    with conn() as c:
        rows = [dict(r) for r in c.execute('SELECT * FROM products')]
    names = {r['id']: strip_accents(r['name']) for r in rows}
    hits = process.extract(strip_accents(a.query), names, scorer=fuzz.WRatio, limit=3, score_cutoff=60)
    return {'ok': True, 'items': [r for r in rows if r['id'] in [h[2] for h in hits]]}

def check_stock(a, s, cfg):
    with conn() as c:
        rows = [dict(r) for r in c.execute('SELECT variant, stock FROM inventory WHERE product_id=?', (a.product_id,))]
    return {'ok': bool(rows), 'code': 'OK' if rows else 'ERR_NOT_FOUND', 'variants': rows}

def _order_for(order_id, phone):
    with conn() as c:
        o = c.execute('SELECT o.*, cu.phone FROM orders o JOIN customers cu ON cu.id=o.customer_id WHERE o.id=?', (order_id,)).fetchone()
    if not o:
        return None, 'ERR_NOT_FOUND'
    if norm_phone(o['phone']) != norm_phone(phone):
        return None, 'ERR_AUTH'      # không tiết lộ thông tin đơn
    return dict(o), 'OK'

def get_order_status(a, s, cfg):
    o, code = _order_for(a.order_id, a.phone)
    if not o:
        return {'ok': False, 'code': code}
    return {'ok': True, 'code': 'OK', 'status': o['status'], 'delivered_at': o['delivered_at'], 'city': o['city']}

FEES_MAP = {
    'ha noi': 20000,
    'tp.hcm': 20000,
    'tphcm': 20000,
    'ho chi minh': 20000,
    'tp ho chi minh': 20000,
    'tp. ho chi minh': 20000,
    'thanh pho ho chi minh': 20000,
    'da nang': 30000,
}

def calc_shipping_fee(a, s, cfg):
    subtotal = 0
    with conn() as c:
        for i in a.items:
            row = c.execute('SELECT price FROM products WHERE id=?', (i.product_id,)).fetchone()
            if row:
                subtotal += row['price'] * i.qty
    city_clean = strip_accents(a.city).strip().lower()
    is_free = subtotal >= 1000000
    fee = 0 if subtotal >= 1000000 else FEES_MAP.get(city_clean, 40000)
    if is_free:
        reason = "Được miễn phí giao hàng do tổng đơn hàng đạt từ 1.000.000đ trở lên"
    else:
        reason = f"Cước phí vẫn chuyển tiêu chuẩn tới {a.city} là {fee:,}đ"
    return {'ok': True, 'subtotal': subtotal, 'fee': fee, 'reason': reason}

def decide_return(o, item, reason):
    if o['status'] == 'cancelled':
        return 'ERR_CANCELLED'
    if o['status'] != 'delivered':
        return 'ERR_NOT_DELIVERED'
    d = days_since(o['delivered_at'])
    if reason == 'defect':
        return 'OK_DEFECT' if d <= 30 else 'ERR_EXPIRED_30D'
    if item['activated']:
        return 'ERR_ACTIVATED'
    if item['opened'] and item['category'] == 'earbuds':
        return 'ERR_OPENED_HYGIENE'
    if d > 7:
        return 'ERR_EXPIRED_7D'
    return 'OK_CHANGE_MIND'

def prepare_return(a, s, cfg):
    o, code = _order_for(a.order_id, a.phone)
    if not o:
        return {'ok': False, 'code': code}
    with conn() as c:
        item = c.execute('SELECT i.*, p.category, p.name FROM order_items i JOIN products p ON p.id=i.product_id WHERE i.order_id=? AND i.product_id=?', (a.order_id, a.product_id)).fetchone()
    if not item:
        return {'ok': False, 'code': 'ERR_ITEM_NOT_IN_ORDER'}
    code = decide_return(o, dict(item), a.reason) if cfg.get('policy_engine', True) else 'OK_CHANGE_MIND'
    if not code.startswith('OK'):
        return {'ok': False, 'code': code}
    token = uuid.uuid4().hex[:8]
    s.pending[token] = {'order_id': a.order_id, 'product_id': a.product_id, 'reason': a.reason}
    return {'ok': True, 'code': code, 'token': token, 'summary': f'Đổi {item["name"]} của đơn {a.order_id}, lý do: {a.reason}'}

def commit_return(a, s, cfg):
    p = s.pending.get(a.token)
    if not p:
        return {'ok': False, 'code': 'ERR_NO_PENDING'}
    if cfg.get('enforce_confirm', True) and not s.last_user_confirmed:
        return {'ok': False, 'code': 'ERR_NEED_CONFIRM', 'message': 'Hãy đọc lại tóm tắt và xin khách xác nhận trước.'}
    s.pending.pop(a.token)
    with conn() as c:
        c.execute('INSERT INTO returns(order_id, product_id, reason, status) VALUES(?,?,?,?)', (p['order_id'], p['product_id'], p['reason'], 'requested'))
    return {'ok': True, 'code': 'OK', 'message': 'Đã tạo yêu cầu đổi trả.'}

def escalate_to_human(a, s, cfg):
    with conn() as c:
        c.execute('INSERT INTO escalations(session_id, reason, summary) VALUES(?,?,?)', (s.id, a.reason, a.summary))
    return {'ok': True, 'code': 'OK'}

TOOLS = {
    'search_products': (SearchIn, search_products, 'Tìm sản phẩm theo tên'),
    'check_stock': (StockIn, check_stock, 'Xem tồn kho theo mã sản phẩm'),
    'get_order_status': (OrderIn, get_order_status, 'Tra trạng thái đơn, cần mã đơn và số điện thoại khách'),
    'calc_shipping_fee': (ShipIn, calc_shipping_fee, 'Tính phí giao hàng'),
    'prepare_return': (PrepareReturnIn, prepare_return, 'Kiểm tra điều kiện đổi trả, trả token, chưa ghi dữ liệu'),
    'commit_return': (CommitIn, commit_return, 'Tạo yêu cầu đổi trả sau khi khách đã xác nhận'),
    'escalate_to_human': (EscalateIn, escalate_to_human, 'Chuyển nhân viên cho khiếu nại hoặc khi khách yêu cầu'),
}

def schemas():
    return [{'name': n, 'description': d, 'input_schema': m.model_json_schema()} for n, (m, f, d) in TOOLS.items()]

def call(name, args, s, cfg):
    if name not in TOOLS:
        return {'ok': False, 'code': 'ERR_UNKNOWN_TOOL'}
    model, fn, _ = TOOLS[name]
    try:
        out = fn(model(**args), s, cfg)
    except Exception as e:
        out = {'ok': False, 'code': 'ERR_BAD_ARGS', 'message': str(e)[:200]}
    s.log.append({'name': name, 'args': args, 'out': out, 'confirmed': s.last_user_confirmed})
    s.last_turn_calls.append({'name': name, 'args': args, 'out': out})
    return out
