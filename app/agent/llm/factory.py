import os
from dotenv import load_dotenv

load_dotenv()

from .base import BaseLLM
from .claude import ClaudeLLM
from .openai_compatible import OpenAICompatLLM
from .mock import MockLLM

def build_llm(provider: str | None = None) -> BaseLLM:
    prov = (provider or os.environ.get('LLM_PROVIDER', 'claude')).lower()
    
    if prov in ('claude', 'anthropic'):
        return ClaudeLLM()
    elif prov == 'groq':
        return OpenAICompatLLM(
            base_url=os.environ.get('GROQ_BASE_URL', 'https://api.groq.com/openai/v1'),
            api_key=os.environ.get('GROQ_API_KEY') or os.environ.get('OPENAI_API_KEY'),
            model=os.environ.get('GROQ_MODEL') or os.environ.get('LLM_MODEL', 'llama-3.3-70b-versatile')
        )
    elif prov == 'openrouter':
        return OpenAICompatLLM(
            base_url=os.environ.get('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
            api_key=os.environ.get('OPENROUTER_API_KEY') or os.environ.get('OPENAI_API_KEY'),
            model=os.environ.get('OPENROUTER_MODEL') or os.environ.get('LLM_MODEL', 'meta-llama/llama-3.3-70b-instruct')
        )
    elif prov in ('openai', 'openai_compat', 'gemini'):
        return OpenAICompatLLM()
    elif prov == 'mock':
        return MockLLM()
    
    return ClaudeLLM()

