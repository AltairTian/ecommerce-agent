"""对话路由 —— Agent 问答接口。"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat():
    """Agent 对话接口 —— 接收用户问题，返回 Agent 分析结果。"""
    # TODO: Phase 1.4 实现
    return {"message": "chat endpoint placeholder"}
