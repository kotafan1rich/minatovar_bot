import traceback
from aiogram import Router
from aiogram.types import ErrorEvent
from config import LOG_ADMIN
from utils.logger import logger
from create_bot import bot
from aiogram.exceptions import TelegramAPIError


error_router = Router(name="error_router")


@error_router.error()
async def errors_handler(event: ErrorEvent):
    MAX_MESSAGE_LENGTH = 4000
    traceback_rormat = traceback.format_exc()

    if len(traceback_rormat) > MAX_MESSAGE_LENGTH:
        traceback_rormat = (
            "[Сообщение сокращено]...\n" + traceback_rormat[MAX_MESSAGE_LENGTH:]
        )
    # Форматируем текст ошибки
    error_message = (
        f"⚠️ *Ошибка в боте*\n\n"
        f"💥 *event*: `{event.exception}`\n\n"
        f"📝 *Traceback*: ```{traceback_rormat}```"
    )

    error__for_logger = (
        f"⚠️ *Ошибка в боте*\n\n"
        f"💥 *event*: `{event}`\n\n"
        f"📝 *Traceback*: ```{traceback_rormat}```"
    )
    logger.error(error__for_logger)  # Логируем ошибку в консоль

    # Пытаемся отправить сообщение в Telegram
    try:
        await bot.send_message(
            chat_id=LOG_ADMIN, text=error_message, parse_mode="Markdown"
        )
    except TelegramAPIError as api_error:
        logger.error(f"Ошибка при отправке сообщения: {api_error}")

    except Exception:
        logger.error("Не удалось отправить сообщение об ошибке. Проверьте ID чата.")

    return True
