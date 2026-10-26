from functools import lru_cache
from langchain_ollama import ChatOllama
from config import MODEL, BASE_URL

@lru_cache(maxsize=1)
def get_llm():
    return ChatOllama(model=MODEL, base_url=BASE_URL, temperature=0)
