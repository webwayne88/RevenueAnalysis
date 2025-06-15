from langchain_gigachat.chat_models import GigaChat
from llm_model.config import LLM_SETTINGS

def get_llm():
    return GigaChat(**LLM_SETTINGS)
