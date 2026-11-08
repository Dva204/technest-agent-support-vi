import os
import sys
import csv
import time
import json
from dotenv import load_dotenv

load_dotenv()

from app.db import reset_db, snapshot
from app.agent.session import Session
from app.agent.loop import run_turn
from app.agent.confirm import strip_accents
from app.agent.llm import build_llm

DEFAULT_FORBIDDEN = {'commit_return', 'escalate_to_human'}

CONFIGS = {
    'A0': {'tools_enabled': False, 'policy_engine': False, 'enforce_confirm': False},
    'A1': {'tools_enabled': True, 'policy_engine': False, 'enforce_confirm': False},
    'A2': {'tools_enabled': True, 'policy_engine': True, 'enforce_confirm': True},
}

def compact_digits(text: str) -> str:
    return ''.join(ch for ch in text if ch.isdigit())

def load_scenarios(path: str) -> list[dict]:
    out = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sc = json.loads(line)
            e = sc.setdefault('expect', {})
            need = set(e.get('tools_called', []))
            e['forbidden_tools'] = sorted(DEFAULT_FORBIDDEN - need)
            out.append(sc)
    return out

def state_matches(expected: dict) -> bool:
    snap = snapshot()
    for table, rows in snap.items():
        want = expected.get(table, [])
        if len(rows) != len(want):
            return False
        for w in want:
            # Check if there is a row in rows matching all keys in w
            if not any(all(r.get(k) == v for k, v in w.items()) for r in rows):
                return False
    return True

def run_scenario(sc: dict, cfg: dict, llm) -> dict:
    reset_db()
    s = Session(id=sc['id'])
    t0 = time.time()
    for turn in sc['turns']:
        run_turn(s, turn['user'], llm, cfg)

    e = sc.get('expect', {})
    called = [c['name'] for c in s.log]

    ok_state = state_matches(e.get('final_db', {}))
    ok_forbidden = not (set(called) & set(e.get('forbidden_tools', [])))
    ok_required = set(e.get('tools_called', [])) <= set(called)
    ok_confirm = all(c['confirmed'] for c in s.log if c['name'] == 'commit_return' and c['out'].get('ok'))

    reply_raw = s.last_reply
    reply_stripped = strip_accents(reply_raw)

    ok_text = True
    if 'reply_must_contain' in e:
        ok_text = ok_text and all(strip_accents(x) in reply_stripped for x in e['reply_must_contain'])
    if 'reply_must_not_contain' in e:
        ok_text = ok_text and not any(strip_accents(x) in reply_stripped for x in e['reply_must_not_contain'])
    if 'reply_must_contain_numbers' in e:
        digits_reply = compact_digits(reply_raw)
        ok_text = ok_text and all(compact_digits(x) in digits_reply for x in e['reply_must_contain_numbers'])

    success = all([ok_state, ok_forbidden, ok_required, ok_confirm, ok_text])

    return {
        'id': sc['id'],
        'category': sc.get('category', ''),
        'success': success,
        'state': ok_state,
        'forbidden': ok_forbidden,
        'required': ok_required,
        'confirm': ok_confirm,
        'text': ok_text,
        'seconds': round(time.time() - t0, 2),
        'tools_called': ','.join(called),
        'last_reply': reply_raw[:150]
    }

if __name__ == '__main__':
    cfg_name = sys.argv[1] if len(sys.argv) > 1 else 'A2'
    split = sys.argv[2] if len(sys.argv) > 2 else 'dev'

    if cfg_name not in CONFIGS:
        print(f"Lỗi: Cấu hình '{cfg_name}' không hợp lệ. Chọn một trong: {list(CONFIGS.keys())}")
        sys.exit(1)

    scenarios_path = f'data/scenarios/{split}.jsonl'
    if not os.path.exists(scenarios_path):
        print(f"Lỗi: Không tìm thấy file kịch bản tại {scenarios_path}")
        sys.exit(1)

    llm = build_llm()
    scenarios = load_scenarios(scenarios_path)
    print(f"Bắt đầu chạy đánh giá [{cfg_name}] trên tập [{split}] ({len(scenarios)} kịch bản)...")

    results = []
    for sc in scenarios:
        res = run_scenario(sc, CONFIGS[cfg_name], llm)
        status_str = "PASS" if res['success'] else "FAIL"
        print(f"  [{res['id']}] {res['category']} -> {status_str} ({res['seconds']}s)")
        results.append(res)

    os.makedirs('experiments', exist_ok=True)
    out_file = f'experiments/{cfg_name}_{split}.csv'
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader()
        w.writerows(results)

    success_cnt = sum(r['success'] for r in results)
    print(f"\n=> Kết quả {cfg_name} [{split}]: {success_cnt}/{len(results)} thành công. Đã lưu báo cáo tại {out_file}")

