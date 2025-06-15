import os

LLM_SETTINGS = { 
        "auth_url" : os.environ["LLM_AUTH_URL"], 
        "scope" : os.environ["LLM_SCOPE"], 
        "credentials": os.environ["LLM_API_KEY"], 
        "verify_ssl_certs": False, 
        "model" : os.environ["LLM_MODEL"] 
}


