from langchain_core.messages import SystemMessage
from llm_model.llm import get_llm


def get_llm_answer(request):
    llm = get_llm()
    prompt = f"""
        Ты финансовый аналитик, который помогает создавать красивые и информативные отчеты в Streamlit. 
        На основе предоставленных данных о выручке компании сгенерируй краткий аналитический отчёт на русском языке в формате Markdown.
        Выдай только сам markdown без пояснений.
        Отчет обязательно должен содержать три блока, разделенных только строкой 'block', без заголовков и названий блоков!:
        1. Блок с основными показателями  
        2. Блок с анализом динамики  
        3. Блок с итоговыми выводами  
        Данные: {request.data}
        """
    messages = [
        SystemMessage(content=prompt),
    ]
    
    response = llm.invoke(messages)
    content = response.content
    return {"analysis": content}

