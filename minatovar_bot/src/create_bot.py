from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from config import TOKEN
from db.connection import REDIS_URL

storage = RedisStorage.from_url(REDIS_URL)

ADMINS = (1019030670, 1324716819, 1423930901)
LOG_ADMIN = 1324716819

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=storage)
