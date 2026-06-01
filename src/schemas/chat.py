"""对话相关的 Pydantic 模型。"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """用户对话请求。"""
    question: str = Field(..., description="用户问题", min_length=1, max_length=5000)
    use_rag: bool = Field(default=False, description="是否启用 RAG 检索增强")
    history: list[dict] | None = Field(
        default=None,
        description="多轮对话历史，格式：[{role: 'user'|'assistant', content: '...'}]",
    )


class ChatResponse(BaseModel):
    """Agent 对话响应。"""
    answer: str = Field(..., description="Agent 分析结果")
    question: str = Field(..., description="原始问题（回显）")
    mode: str = Field(default="default", description="响应模式：default | rag")
