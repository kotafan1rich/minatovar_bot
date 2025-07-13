from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.db.models import OrderTypeItem

class BaseKeyboards:
    BACK_BOTTON = InlineKeyboardButton(text="◀️", callback_data="back")
    CLOSE_BOTTON = InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    GET_CLOTH_BOTTON = InlineKeyboardButton(
        text=OrderTypeItem.CLOTH.value,
        callback_data=f"type_{OrderTypeItem.CLOTH.value}",
    )
    GET_SHOES_BOTTON = InlineKeyboardButton(
        text=OrderTypeItem.SHOES.value,
        callback_data=f"type_{OrderTypeItem.SHOES.value}",
    )

    @classmethod
    def close_inline(cls):
        return InlineKeyboardMarkup(inline_keyboard=[[cls.CLOSE_BOTTON]])

    @classmethod
    def get_type_item_inline(cls):
        bottons = [[cls.GET_SHOES_BOTTON, cls.GET_CLOTH_BOTTON], [cls.CLOSE_BOTTON]]
        return InlineKeyboardMarkup(inline_keyboard=bottons)
