import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram.types import BotCommand
from aiogram.types.update import Update
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.config import settings
from src.create_bot import bot, dp
from src.db.dals import SettingsDAL
from src.db.session import async_session
from src.handlers import admin_router, client_router, error_router, order_roter
from src.middlewares.middleware import (
    CallbackDataMiddleware,
    DBSessionMiddleware,
    StartMiddleware,
)


async def on_startapp():
    await bot.delete_webhook()

    await bot.set_my_commands([BotCommand(command="/start", description="Начать")])

    params = ("current_rate", "shoes_price", "cloth_price")
    async with async_session() as session:
        settings_dal = SettingsDAL(session)
        for param in params:
            if not await settings_dal.param_exists(param):
                await settings_dal.set_param(param, 0.0)

    dp.update.outer_middleware(DBSessionMiddleware())
    admin_router.callback_query.middleware.register(CallbackDataMiddleware())
    order_roter.callback_query.middleware.register(CallbackDataMiddleware())
    client_router.message.middleware.register(StartMiddleware())
    client_router.callback_query.middleware.register(CallbackDataMiddleware())

    dp.include_router(error_router)
    dp.include_router(client_router)
    dp.include_router(order_roter)
    dp.include_router(admin_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startapp()

    if settings.DEBUG:
        await bot.set_webhook(
            url=f"{settings.BASE_URL}{settings.WEBHOOK_PATH}",
            secret_token=settings.SECRET_KEY,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logging.info(f"Webhook set to {settings.BASE_URL}{settings.WEBHOOK_PATH}")
    yield

    await bot.delete_webhook()
    logging.info("Webhook removed")


app = FastAPI(title="MinatovarAPI", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=settings.STATIC_FILES), name="static")
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)


async def verify_webhook_token(
    x_telegram_token: str = Header(..., alias="X-Telegram-Bot-Api-Secret-Token"),
):
    if x_telegram_token != settings.SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


@app.post(f"{settings.WEBHOOK_PATH}", include_in_schema=False)
async def webhook(
    request: Request, is_valid_token: bool = Depends(verify_webhook_token)
) -> None:
    update = await request.json()
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot, update)


@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


async def polling():
    await dp.emit_startup(await on_startapp())
    await dp.start_polling(bot)


if __name__ == "__main__":
    if settings.DEBUG:
        asyncio.run(polling())
    else:
        uvicorn.run(app, host=settings.HOST, port=settings.PORT)
