from dataclasses import dataclass, field

@dataclass
class Session:
    id: str
    messages: list = field(default_factory=list)
    pending: dict = field(default_factory=dict)   # token -> dữ liệu yêu cầu đổi trả đang chờ
    last_user_confirmed: bool = False
    log: list = field(default_factory=list)       # nhật ký công cụ
    last_reply: str = ''
    last_turn_calls: list = field(default_factory=list)