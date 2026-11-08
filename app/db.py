import os
import shutil
import sqlite3
from dotenv import load_dotenv

load_dotenv()

SEED = 'data/shop/seed.db'

def db_path():
    return os.environ.get('DB_PATH', 'data/shop/work.db')

def reset_db():
    target = db_path()
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    shutil.copyfile(SEED, target)

def conn():
    c = sqlite3.connect(db_path())
    c.row_factory = sqlite3.Row
    return c

def snapshot():
    # chỉ các bảng agent được phép ghi
    with conn() as c:
        out = {}
        for t in ('returns', 'escalations'):
            out[t] = [dict(r) for r in c.execute(f'SELECT * FROM {t} ORDER BY id')]
        return out

def diff(before, after):
    return {t: after[t][len(before[t]):] for t in after}
