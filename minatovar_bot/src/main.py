from contextlib import asynccontextmanager
import logging
import asyncio
from aiogram.types import BotCommand
from aiogram.types.update import Update
from fastapi import Depends, FastAPI, HTTPException, Header, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from create_bot import bot, dp
from db.dals import SettingsDAL
from handlers import admin_router, client_router, order_roter, error_router
from db.session import async_session
from middlewares.middleware import (
    DBSessionMiddleware,
    StartMiddleware,
    CallbackDataMiddleware,
)
from config import (
    BASE_URL,
    HOST,
    PORT,
    STATIC_FILES,
    TEMPLATE_DIR,
    WEBHOOK_PATH,
    DEBUG,
    SECRET_KEY,
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

    await bot.set_webhook(
        url=f"{BASE_URL}{WEBHOOK_PATH}",
        secret_token=SECRET_KEY,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {BASE_URL}{WEBHOOK_PATH}")
    yield

    await bot.delete_webhook()
    logging.info("Webhook removed")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_FILES), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


async def verify_webhook_token(
    x_telegram_token: str = Header(..., alias="X-Telegram-Bot-Api-Secret-Token"),
):
    if x_telegram_token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


@app.post(f"{WEBHOOK_PATH}")
async def webhook(
    request: Request, is_valid_token: bool = Depends(verify_webhook_token)
) -> None:
    update = await request.json()
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot, update)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


async def polling():
    await dp.emit_startup(await on_startapp())
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        asyncio.run(polling())
    else:
        uvicorn.run(app, host=HOST, port=PORT)
