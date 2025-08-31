import traceback

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent
from src.config import LOG_ADMIN
from src.create_bot import bot
from src.utils.logger import logger

error_router = Router(name="error_router")


@error_router.error()
async def errors_handler(event: ErrorEvent):
    MAX_MESSAGE_LENGTH = 4000
    traceback_format = traceback.format_exc()

    error_for_logger = (
        f"⚠️ *Ошибка в боте*\n\n"
        f"💥 *event*: `{event}`\n\n"
        f"📝 *Traceback*: ```{traceback_format}```"
    )
    logger.error(error_for_logger)  # Логируем ошибку в консоль

    if len(traceback_format) > MAX_MESSAGE_LENGTH:
        traceback_format = (
            "[Сообщение сокращено]...\n" + traceback_format[MAX_MESSAGE_LENGTH:]
        )
    # Форматируем текст ошибки
    error_message = (
        f"⚠️ *Ошибка в боте*\n\n"
        f"💥 *event*: `{event.exception}`\n\n"
        f"📝 *Traceback*: ```{traceback_format}```"
    )

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
