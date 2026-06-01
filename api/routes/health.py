"""健康检查路由 —— 监控探针、就绪检查、依赖服务探测。"""

import time
import logging

from fastapi import APIRouter, Request

from db.connection import get_connection
from config.settings import OLLAMA_BASE_URL

logger = logging.getLogger("api")
router = APIRouter()

# 服务启动时间（由 lifespan 设置，用于计算 uptime）
_start_time: float | None = None


def set_start_time(t: float) -> None:
    """由 lifespan 在启动时调用，记录服务启动时间。"""
    global _start_time
    _start_time = t


def _uptime_seconds() -> float:
    """返回服务已运行秒数。"""
    if _start_time is None:
        return 0
    return time.time() - _start_time


def _check_database() -> dict:
    """检查数据库连接是否正常。"""
    try:
        conn = get_connection()
        try:
            conn.execute("SELECT 1")
        finally:
            conn.close()
        return {"status": "ok"}
    except Exception as e:
        logger.warning("Database health check failed: %s", e)
        return {"status": "error", "detail": str(e)}


def _check_ollama() -> dict:
    """检查 Ollama 服务是否可达。"""
    import httpx
    try:
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            return {"status": "ok", "base_url": OLLAMA_BASE_URL, "models": models}
        return {"status": "error", "detail": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"status": "unreachable", "detail": str(e)}


@router.get("/health")
async def health_check(request: Request):
    """服务健康检查端点 —— 返回服务状态和依赖服务探测结果。"""
    db = _check_database()
    ollama = _check_ollama()

    overall = "ok" if db["status"] == "ok" else "degraded"

    return {
        "status": overall,
        "version": request.app.version,
        "uptime_seconds": round(_uptime_seconds(), 1),
        "checks": {
            "database": db,
            "ollama": ollama,
        },
    }
