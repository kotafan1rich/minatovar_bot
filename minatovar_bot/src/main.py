from contextlib import asynccontextmanager
import logging
from aiogram.types import BotCommand
from aiogram.types.update import Update
from fastapi import FastAPI, Request
import uvicorn
from create_bot import bot, dp
from db.dals import SettingsDAL
from handlers import admin_router, client_router, order_roter
from db.session import async_session
from middlewares.middleware import (
    DBSessionMiddleware,
    StartMiddleware,
    CallbackDataMiddleware,
)
from config import BASE_URL, HOST, PORT, WEBHOOK_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_my_commands([BotCommand(command="/start", description="Начать")])

    async with async_session() as session:
        settings_dal = SettingsDAL(session)
        if not await settings_dal.param_exists("current_rate"):
            await settings_dal.set_param("current_rate", 0.0)
        if not await settings_dal.param_exists("shoes_price"):
            await settings_dal.set_param("shoes_price", 0.0)
        if not await settings_dal.param_exists("cloth_price"):
            await settings_dal.set_param("cloth_price", 0.0)

    dp.update.outer_middleware(DBSessionMiddleware())
    admin_router.callback_query.middleware.register(CallbackDataMiddleware())
    order_roter.callback_query.middleware.register(CallbackDataMiddleware())
    client_router.message.middleware.register(StartMiddleware())
    client_router.callback_query.middleware.register(CallbackDataMiddleware())

    dp.include_router(client_router)
    dp.include_router(order_roter)
    dp.include_router(admin_router)

    await bot.set_webhook(
        url=f"{BASE_URL}{WEBHOOK_PATH}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {BASE_URL}{WEBHOOK_PATH}")
    yield  # Приложение работает
    # Код, выполняющийся при завершении работы приложения
    await bot.delete_webhook()
    logging.info("Webhook removed")


# Инициализация FastAPI с методом жизненного цикла
app = FastAPI(lifespan=lifespan)


# Маршрут для обработки вебхуков
@app.post(f"{WEBHOOK_PATH}")
async def webhook(request: Request) -> None:
    update = await request.json()
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    uvicorn.run(app, host=HOST, port=PORT)

