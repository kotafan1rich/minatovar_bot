from src.config import settings

from redis.asyncio import Redis

redis_client = Redis(
    host=settings.REDIS_HOST,
    password=settings.REDIS_PASSWORD,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    username=settings.REDIS_USER,
)
