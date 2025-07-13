from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from src.config import get_redis_url, settings

storage = RedisStorage.from_url(get_redis_url())

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=storage)
