import pytest
from app.agent.confirm import is_confirmation

def test_affirmations():
    assert is_confirmation("Đúng rồi, xác nhận giúp tôi.")
    assert is_confirmation("Đúng rồi.")
    assert is_confirmation("Đồng ý!")
    assert is_confirmation("ok")
    assert is_confirmation("Vâng, tiến hành đi")
    assert is_confirmation("Chuẩn rồi")
    assert is_confirmation("xác nhận")

def test_negations():
    assert not is_confirmation("Không, thôi")
    assert not is_confirmation("Không.")
    assert not is_confirmation("Để tôi suy nghĩ thêm.")
    assert not is_confirmation("Hủy giúp tôi")
    assert not is_confirmation("Khoan đã")
    assert not is_confirmation("Chưa")
    assert not is_confirmation("Sai rồi")

def test_negation_overrides_affirmation():
    # Câu có từ phủ định kèm từ khẳng định phải trả về False
    assert not is_confirmation("Không, không đồng ý")
    assert not is_confirmation("Khoan, chưa xác nhận")

