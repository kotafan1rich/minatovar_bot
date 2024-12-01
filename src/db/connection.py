from config import REDIS_HOST, REDIS_DB, REDIS_PORT, REDIS_PASSWORD, REDIS_USER

import redis


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    username=REDIS_USER,
)
REDIS_URL = (
    f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)
