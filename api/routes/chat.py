"""对话路由 —— Agent 问答接口（单轮 / 多轮 / RAG 增强）。"""

import logging

from fastapi import APIRouter, HTTPException

from src.agent.agent import run_agent, run_agent_with_history
from src.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger("api")
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Agent 对话接口。

    接收用户问题，调用 LangChain Agent 进行分析，返回结构化结果。

    支持模式：
    - 默认模式：直接调用 Agent + 工具集
    - RAG 模式（use_rag=true）：检索知识库后增强回答（RAG 未就绪时自动降级）
    - 多轮对话（history 非空）：携带历史上下文
    """
    question = req.question.strip()

    try:
        if req.use_rag:
            # TODO: Phase 3 — 替换为 RAG 增强调用
            logger.info("RAG mode requested but not yet available, falling back to default")
            answer = _call_agent(question, req.history)
            mode = "default (rag fallback)"
        elif req.history:
            answer = run_agent_with_history(question, req.history)
            mode = "multi_turn"
        else:
            answer = _call_agent(question, req.history)
            mode = "default"

        return ChatResponse(answer=answer, question=question, mode=mode)

    except Exception as e:
        logger.exception("Agent call failed for question: %s", question[:100])
        raise HTTPException(
            status_code=500,
            detail=f"Agent 调用失败：{str(e)}",
        )


def _call_agent(question: str, history: list[dict] | None) -> str:
    """统一的 Agent 调用入口，支持多轮历史。"""
    if history:
        return run_agent_with_history(question, history)
    return run_agent(question)
