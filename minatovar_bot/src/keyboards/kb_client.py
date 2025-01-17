from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .common import BaseKeyboards


class ClientKeyboards(BaseKeyboards):
    GET_PRCIE_BOTTON = InlineKeyboardButton(
        text="Рассчитать стоимость товара", callback_data="getprice"
    )
    GET_CURRENT_RATE_BOTTON = InlineKeyboardButton(
        text="Текущий курс юаня", callback_data="getrate"
    )
    ORDER_BOTTON = InlineKeyboardButton(text="Заказы", callback_data="orders")
    REFERRAL_MENU_BOTTON = InlineKeyboardButton(
        text="Рефералы", callback_data="referralmenu"
    )
    promos_BOTTON = InlineKeyboardButton(text="Акции", callback_data="promosclient")
    HELP_BOTTON = InlineKeyboardButton(text="Помощь", callback_data="help")
    MY_REFERRALS_BOTTON = InlineKeyboardButton(
        text="Мои рефералы", callback_data="myreferrals"
    )
    REFERRAL_URL_BOTTON = InlineKeyboardButton(
        text="Моя ссылка", callback_data="referralurl"
    )

    @classmethod
    def main_menu_inline_kb(cls):
        bottons = [
            [cls.GET_PRCIE_BOTTON],
            [cls.GET_CURRENT_RATE_BOTTON],
            [cls.ORDER_BOTTON, cls.REFERRAL_MENU_BOTTON],
            [cls.promos_BOTTON],
            [cls.HELP_BOTTON],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def get_referral_menu_inline(cls):
        bottons = [
            [cls.REFERRAL_URL_BOTTON, cls.MY_REFERRALS_BOTTON],
            [cls.CLOSE_BOTTON],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)
