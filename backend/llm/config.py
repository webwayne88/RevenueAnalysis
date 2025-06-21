import os
from yaml import safe_load

LLM_SETTINGS = { 
        "auth_url" : os.environ["LLM_AUTH_URL"], 
        "scope" : os.environ["LLM_SCOPE"], 
        "credentials": os.environ["LLM_API_KEY"], 
        "verify_ssl_certs": False, 
        "model" : os.environ["LLM_MODEL"] 
}


with open("backend/llm/promts.yaml",  "r",encoding="utf-8") as f:
    prompts = safe_load(f)


MAIN_SYSTEM_PROMPT = prompts["main_system_prompt"]