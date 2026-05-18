from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

import os

# 关键：让 Python 不要把本地 Ollama 请求走代理
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://127.0.0.1:11434",
    temperature=0.7,
)

response = llm.invoke("什么是大语言模型？请用中文简短回答。")
print(response.content)

# # 测试单轮对话
# messages = [HumanMessage(content="你好，请介绍一下你自己")]
# response = llm.invoke(messages)
# def main():
#     print(response.content)
#
# if __name__ == "__main__":
#     main()
