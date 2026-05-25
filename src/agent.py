"""
Agent 核心模块 —— 项目中 Agent 的唯一创建和调用入口。

无论是 Streamlit、CLI、FastAPI 还是测试脚本，
一律通过这里的 run_agent() / run_agent_with_history() 调用。
"""

from typing import Any, Dict, List, Optional

from langchain.agents import create_agent
from langsmith import traceable

from config.llm import llm
from src.tools import tools
from src.prompts import SYSTEM_PROMPT

# Agent 实例（模块级别单例）
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)


def extract_answer(result: Any) -> str:
    """从 LangChain Agent 返回结果中提取最终回答文本。"""
    if result is None:
        return "Agent 没有返回结果。"

    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        messages = result.get("messages")
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", None)
            if content:
                return str(content)
            if isinstance(last_message, dict):
                return str(last_message.get("content", last_message))
        return str(result)

    return str(result)


@traceable(name="ecommerce_agent_run")
def run_agent(user_query: str) -> str:
    """
    单轮 Agent 调用入口。

    用法：
        answer = run_agent("当前总 GMV 是多少？")
        print(answer)
    """
    if not user_query or not user_query.strip():
        return "请输入有效的问题。"

    result = agent.invoke({
        "messages": [{"role": "user", "content": user_query}]
    })
    return extract_answer(result)


@traceable(name="ecommerce_agent_chat")
def run_agent_with_history(
    user_query: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    多轮对话入口。

    history 格式：
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    if history is None:
        history = []

    messages = history + [{"role": "user", "content": user_query}]
    result = agent.invoke({"messages": messages})
    return extract_answer(result)


def print_agent_info() -> None:
    """打印 Agent 配置信息，用于排查环境问题。"""
    from config.settings import (
        OLLAMA_MODEL, OLLAMA_BASE_URL,
        LANGSMITH_TRACING, LANGSMITH_PROJECT, LANGSMITH_ENDPOINT, LANGSMITH_API_KEY,
    )

    print("========== Agent 配置信息 ==========")
    print("OLLAMA_MODEL:", OLLAMA_MODEL)
    print("OLLAMA_BASE_URL:", OLLAMA_BASE_URL)
    print("LANGSMITH_TRACING:", LANGSMITH_TRACING)
    print("LANGSMITH_PROJECT:", LANGSMITH_PROJECT)
    print("LANGSMITH_ENDPOINT:", LANGSMITH_ENDPOINT)
    print("LANGSMITH_API_KEY exists:", bool(LANGSMITH_API_KEY))
    print("Tools count:", len(tools))
    print("===================================")
