from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_DB, REDIS_PORT, REDIS_PASSWORD, REDIS_USER

REDIS_URL = (
    f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)

redis_client = Redis(
    host=REDIS_HOST,
    password=REDIS_PASSWORD,
    port=REDIS_PORT,
    db=REDIS_DB,
    username=REDIS_USER,
)
