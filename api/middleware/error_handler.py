"""全局异常处理器 —— 统一将未捕获异常转为结构化 JSON 响应。"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("api")


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """捕获所有未处理的异常，返回 500 和结构化错误信息。"""
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "服务器内部错误，请稍后重试。",
            "detail": str(exc),
        },
    )
