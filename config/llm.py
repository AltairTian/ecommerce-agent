"""LLM 唯一创建入口 —— 项目中只在这里创建 ChatOllama 实例。"""

import os
from langchain_ollama import ChatOllama
from config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, OLLAMA_TEMPERATURE

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=OLLAMA_TEMPERATURE,
)
