from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.models import OrderStatus

from .common import BaseKeyboards


class AdminKeyboards(BaseKeyboards):
    ALL_ACTIVE_ORDERS_BOTTON = InlineKeyboardButton(
        text="🔁 Активные заказы", callback_data="admin_active"
    )
    ALL_COMPLETED_ORDERS_BOTTON = InlineKeyboardButton(
        text="✅ Завершенные заказы", callback_data="admin_completed"
    )
    promos_BOTTON = InlineKeyboardButton(text="Акции", callback_data="promosadmin")
    ADD_promos_BOTTON = InlineKeyboardButton(
        text="Добавить акцию", callback_data="addpromos"
    )
    ALL_promos_BOTTON = InlineKeyboardButton(
        text="Все акции", callback_data="allpromosadmin"
    )
    CHANGE_SETTINGS_BOTTON = InlineKeyboardButton(
        text="Изменить цены", callback_data="changesettings"
    )
    SHOES_PRCIE_BOTTON = InlineKeyboardButton(
        text="Обувь", callback_data="settings_shoes"
    )
    CLOTH_PRCIE_BOTTON = InlineKeyboardButton(
        text="Одежда", callback_data="settings_cloth"
    )
    CURRENT_RATE_BOTTON = InlineKeyboardButton(
        text="Курс", callback_data="settings_rate"
    )
    BACK_TO_ADMIN_MENU = InlineKeyboardButton(text="◀️", callback_data="adminback")

    @classmethod
    def admin_menu_inline(cls):
        bottons = [
            [cls.ALL_ACTIVE_ORDERS_BOTTON],
            [cls.ALL_COMPLETED_ORDERS_BOTTON],
            [cls.CHANGE_SETTINGS_BOTTON, cls.promos_BOTTON],
            [cls.BACK_BOTTON],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def admin_promos_menu(cls):
        bottons = [
            [cls.ALL_promos_BOTTON],
            [cls.ADD_promos_BOTTON],
            [cls.BACK_TO_ADMIN_MENU],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def get_info_promo_inline(cls, id: int):
        REMOVE_BOTTON = InlineKeyboardButton(
            text="Удалить акцию", callback_data=f"removepromo_{id}"
        )
        bottons = [[REMOVE_BOTTON]]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def get_info_order_inline(cls, id: int):
        CHANGE_STATUS_BOTTON = InlineKeyboardButton(
            text="Изменить статус", callback_data=f"status_{id}"
        )
        REMOVE_BOTTON = InlineKeyboardButton(
            text="Удалить заказ", callback_data=f"removeorder_{id}"
        )
        bottons = [[CHANGE_STATUS_BOTTON], [REMOVE_BOTTON]]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def get_status_order_inline(cls, id: int):
        bottons = [
            [
                InlineKeyboardButton(
                    text=f"{status.value}",
                    callback_data=f"chstatus_{status.value}_{id}",
                )
            ]
            for status in OrderStatus
        ]
        bottons.append(
            [InlineKeyboardButton(text="◀️", callback_data=f"backorder_{id}")]
        )
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def change_settings_admin_inline(cls):
        bottons = [
            [cls.SHOES_PRCIE_BOTTON, cls.CLOTH_PRCIE_BOTTON],
            [cls.CURRENT_RATE_BOTTON],
            [cls.BACK_TO_ADMIN_MENU],
        ]
        return InlineKeyboardMarkup(inline_keyboard=bottons)

    @classmethod
    def back_to_admin_menu_inline(cls):
        return InlineKeyboardMarkup(inline_keyboard=[[cls.BACK_TO_ADMIN_MENU]])
