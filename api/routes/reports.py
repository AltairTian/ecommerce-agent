"""报告路由 —— 经营报告查询接口。"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/reports")
async def list_reports():
    """列出可用的报告类型。"""
    # TODO: Phase 1.5 实现
    return {"message": "reports endpoint placeholder"}
