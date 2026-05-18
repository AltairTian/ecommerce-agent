
import os
from langchain_ollama import ChatOllama

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://127.0.0.1:11434",
    temperature=0.3,
)