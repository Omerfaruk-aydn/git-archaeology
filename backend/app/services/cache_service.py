import json
from typing import Optional, Any
from functools import wraps

from app.core.config import settings

_redis_client = None


def _get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    try:
        import redis
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        _redis_client.ping()
        return _redis_client
    except Exception:
        _redis_client = _NoCache()
        return _redis_client


class _NoCache:
    def get(self, key): return None
    def set(self, *a, **kw): pass
    def delete(self, *a, **kw): pass
    def keys(self, *a, **kw): return []
    def setex(self, *a, **kw): pass


class CacheService:
    def __init__(self):
        self.redis = _get_redis()
        self.default_ttl = 3600

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            if isinstance(value, str):
                return json.loads(value)
            return value
        return None

    def set(self, key: str, value: Any, ttl: int = None):
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value, default=str),
        )

    def delete(self, key: str):
        self.redis.delete(key)

    def invalidate_pattern(self, pattern: str):
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)


def cache_result(key_prefix: str, ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = CacheService()
            cache_key = f"{key_prefix}:{hash(str(args) + str(kwargs))}"

            cached = cache.get(cache_key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
