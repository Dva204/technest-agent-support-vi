import re
import unicodedata

def strip_accents(s: str) -> str:
    s = s.lower().replace('đ', 'd')
    s = unicodedata.normalize('NFD', s)
    return ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')

AFFIRM = ['co', 'dong y', 'xac nhan', 'ok', 'oke', 'dung roi', 'vang', 'duoc', 'chuan', 'chinh xac']
NEG = ['khong', 'thoi', 'huy', 'khoan', 'de toi nghi', 'chua', 'sai']

def is_confirmation(text: str) -> bool:
    cleaned = re.sub(r'[^\w\s]', ' ', strip_accents(text))
    t = ' ' + ' '.join(cleaned.split()) + ' '
    if any(' ' + w + ' ' in t for w in NEG):
        return False
    return any(' ' + w + ' ' in t for w in AFFIRM)
