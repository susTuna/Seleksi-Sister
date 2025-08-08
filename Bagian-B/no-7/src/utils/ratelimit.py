from cachetools import TTLCache
from fastapi import HTTPException, status, Request, Depends
from api.token.token import get_current_client
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.logger import log_usage
import time

RATE_LIMIT = {
    "default": {"calls": 60, "period": 60},  # 60 calls per minute
    "/detect": {"calls": 30, "period": 60},  # 30 calls per minute
    "/custom-words": {"calls": 20, "period": 60},  # 20 calls per minute
}

cache = TTLCache(maxsize=1000, ttl=60)  # Cache for 1 minute

async def rate_limiter(request: Request, client: str = Depends(get_current_client)):
    client_id = client.client_id
    path = request.url.path
    limit_config = RATE_LIMIT.get(path, RATE_LIMIT["default"])
    max_calls = limit_config["calls"]
    period = limit_config["period"]

    if client_id not in cache:
        cache[client_id] = {}
    if path not in cache[client_id]:
        cache[client_id][path] = {"count": 0, "reset_at": time.time() + period}

    client_count = cache[client_id][path]
    if client_count["count"] >= max_calls:
        error_msg = f"Rate limit exceeded: {max_calls} requests per {period} seconds"
        content_length = request.headers.get('Content-Length')
        size = int(content_length) if content_length else 0
        log_usage(client_id, path, size, False, error_msg)
        retry_after = int(client_count["reset_at"] - time.time())
        headers = {
             "X-RateLimit-Limit": str(max_calls),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(int(client_count["reset_at"])),
            "Retry-After": str(retry_after if retry_after > 0 else 1)
        }
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_msg,
            headers=headers
        )
    client_count["count"] += 1

    request.state.rate_limit_headers = {
        "X-RateLimit-Limit": str(max_calls),
        "X-RateLimit-Remaining": str(max_calls - client_count["count"]),
        "X-RateLimit-Reset": str(int(client_count["reset_at"])),
    }
    return client