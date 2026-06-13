from pydantic import BaseModel
from browser_use.llm import BaseChatModel

class LLMConfig(BaseModel):
    llm: BaseChatModel
    page_extraction_llm: BaseChatModel
    fallback_llm: BaseChatModel
    judge_llm: BaseChatModel
    flash_mode: bool
    use_vision: bool
    max_failures: int