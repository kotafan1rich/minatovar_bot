from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.keyboards.common import BaseKeyboards


class OrderKeyboards(BaseKeyboards):
    CREATE_ORDER_BOTTON = InlineKeyboardButton(
        text="✏️ Сделать заказ", callback_data="createorder"
    )
    MY_ORDERS_BOTTON = InlineKeyboardButton(
        text="📜 Мои заказы", callback_data="myorders"
    )
    CONFRIM_BOTTON = InlineKeyboardButton(text="Да всё верно", callback_data="confrim")
    BACK_TO_ORDERS_BOTTON = InlineKeyboardButton(text="◀️", callback_data="backtoorders")

    @classmethod
    def order_menu_inline(cls):
        bottons = [[cls.CREATE_ORDER_BOTTON, cls.MY_ORDERS_BOTTON], [cls.BACK_BOTTON]]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def confrim_inline(cls):
        bottons = [[cls.CONFRIM_BOTTON], [cls.BACK_TO_ORDERS_BOTTON]]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def cancel_inline(cls):
        return InlineKeyboardMarkup(inline_keyboard=[[cls.CANCEL_BOTTON]])

    @classmethod
    def back_to_orders_inline(cls):
        return InlineKeyboardMarkup(inline_keyboard=[[cls.BACK_TO_ORDERS_BOTTON]])

    @classmethod
    def get_type_item_inline(cls):
        bottons = [
            [cls.GET_SHOES_BOTTON, cls.GET_CLOTH_BOTTON],
            [cls.BACK_TO_ORDERS_BOTTON],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)
