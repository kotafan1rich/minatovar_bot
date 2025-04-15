from aiogram.types import InputMediaPhoto, FSInputFile

from config import STATIC_FILES
from handlers.messages import SEND_PRICE


def get_media_group_shoes():
    return [
        InputMediaPhoto(media=FSInputFile(f"{STATIC_FILES}/shoes_price_2.jpg")),
        InputMediaPhoto(
            media=FSInputFile(f"{STATIC_FILES}/shoes_price.jpg"),
            caption=SEND_PRICE,
        ),
    ]


def get_media_group_cloth():
    return [
        InputMediaPhoto(media=FSInputFile(f"{STATIC_FILES}/cloth_price_2.jpg")),
        InputMediaPhoto(
            media=FSInputFile(f"{STATIC_FILES}/cloth_price.jpg"),
            caption=SEND_PRICE,
        ),
    ]
