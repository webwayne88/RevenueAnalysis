from langchain_core.messages import SystemMessage
from llm.connection import get_llm
from llm.config import MAIN_SYSTEM_PROMPT

def get_llm_answer(revenue_data):
    llm = get_llm()
    messages = [
        SystemMessage(content=MAIN_SYSTEM_PROMPT.format(data=revenue_data)),
    ]
    response = llm.invoke(messages)
    content = response.content
    return {"analysis": content}

