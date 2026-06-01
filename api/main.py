"""
FastAPI 应用入口 —— 电商数据分析 Agent 的 API 服务。

启动方式：
    uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, chat, reports


# ── 应用生命周期 ────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的资源管理。"""
    # 启动时：验证配置、预热连接等
    from config.settings import print_config
    print_config()
    yield
    # 关闭时：清理资源（数据库连接池、向量存储等）
    pass


# ── FastAPI 实例 ────────────────────────────────────

app = FastAPI(
    title="电商数据分析 Agent",
    description=(
        "基于 LangChain + Ollama 的电商数据分析 API，"
        "支持自然语言查询、图表生成、经营报告，以及 RAG 检索增强。"
    ),
    version="0.2.0",
    lifespan=lifespan,
)


# ── CORS 中间件 ────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 开发阶段允许所有来源，生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 注册路由 ────────────────────────────────────────

app.include_router(health.router, prefix="/api", tags=["健康检查"])
app.include_router(chat.router, prefix="/api", tags=["对话"])
app.include_router(reports.router, prefix="/api", tags=["报告"])


# ── 根路径 ──────────────────────────────────────────

@app.get("/")
async def root():
    """API 根路径，返回服务信息和文档链接。"""
    return {
        "service": "电商数据分析 Agent API",
        "version": app.version,
        "docs": "/docs",
        "health": "/api/health",
    }


# ── 直接启动 ────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    from config.settings import API_HOST, API_PORT
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)
