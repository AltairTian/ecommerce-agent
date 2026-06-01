"""健康检查路由 —— 监控探针、就绪检查。"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """服务健康检查端点。"""
    return {"status": "ok"}
