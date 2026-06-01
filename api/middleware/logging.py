"""请求日志中间件 —— 记录每个请求的方法、路径、状态码和耗时。"""

import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """记录每个 HTTP 请求的基本信息和耗时。"""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "%s %s → %s (%.0fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
