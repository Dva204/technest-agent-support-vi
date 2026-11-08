from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class LLMResult:
    text: str
    tool_calls: list = field(default_factory=list)  # mỗi phần tử: {'id':..., 'name':..., 'input':{...}}
    raw_content: object = None                      # nội dung để đưa lại vào lịch sử
    in_tokens: int = 0
    out_tokens: int = 0

class BaseLLM(ABC):
    @abstractmethod
    def chat(self, system: str, messages: list, tools: list | None) -> LLMResult:
        """Thực thi gọi LLM với prompt hệ thống, lịch sử tin nhắn và danh sách công cụ."""
        pass

