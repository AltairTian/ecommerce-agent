"""LangSmith 连通性测试。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.llm import llm
from langsmith import traceable


@traceable(name="langsmith_ollama_test")
def run_test():
    response = llm.invoke("请用一句中文回答：LangSmith 是做什么的？")
    return response.content


if __name__ == "__main__":
    print("=== LangSmith 连通性测试 ===")
    result = run_test()
    print("模型返回:", result)
