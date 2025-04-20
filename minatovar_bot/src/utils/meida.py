from aiogram.types import FSInputFile, InputMediaPhoto
from config import MEDIA_FILES
from handlers.messages import SEND_PRICE


def get_media_group_shoes():
    return [
        InputMediaPhoto(media=FSInputFile(f"{MEDIA_FILES}/shoes_price_2.jpg")),
        InputMediaPhoto(
            media=FSInputFile(f"{MEDIA_FILES}/shoes_price.jpg"),
            caption=SEND_PRICE,
        ),
    ]


def get_media_group_cloth():
    return [
        InputMediaPhoto(media=FSInputFile(f"{MEDIA_FILES}/cloth_price_2.jpg")),
        InputMediaPhoto(
            media=FSInputFile(f"{MEDIA_FILES}/cloth_price.jpg"),
            caption=SEND_PRICE,
        ),
    ]
