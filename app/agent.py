from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from app.tools.agent_tool import tools


# ======================
# LLM（ollama本地部署的qwen3：8b）
# ======================

from app.llm import llm


# ======================
# Tool
# ======================

@tool
def total_gmv_tool() -> str:
    """
    查询总GMV
    """
    return "当前总GMV为 1280万元"


@tool
def top_category_tool() -> str:
    """
    查询销量最高品类
    """
    return "销量最高品类为：电子产品"


# tools = [
#     total_gmv_tool,
#     top_category_tool
# ]


# ======================
# Agent
# ======================

agent = create_agent(
    llm,
    tools
)


# ======================
# Test
# ======================

response = agent.invoke(
    {
        "messages": [
            ("user", "请生成一份完整的电商经营分析报告")
        ]
    }
)


print(response["messages"][-1].content)
