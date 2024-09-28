from functools import lru_cache


from langchain_openai import ChatOpenAI


@lru_cache(maxsize=1)
def get_model() -> ChatOpenAI:
    return ChatOpenAI()
