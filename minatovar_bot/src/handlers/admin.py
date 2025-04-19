from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ADMINS
from create_bot import bot
from db.dals import OrderDAL, PromosDAL, SettingsDAL, UserDAL
from db.models import OrderStatus
from fsms import FSMAdmin
from keyboards import AdminKeyboards
from sqlalchemy.ext.asyncio import AsyncSession

from .messages import (
    BAD_FORMAT_ERROR,
    NO_ORDERS,
    NO_PROMOS,
    NON_ARGUMENT_ERROR,
    SEND_COMMAND,
    SEND_DESCRIPTION,
    SEND_NEW_VALUE,
    WHAT_CHANGE_QUSTION,
    WHATS_NEXT,
    get_order_for_admin,
    get_promos,
)

admin_router = Router(name="admin_router")


@admin_router.message(Command("admin"), F.from_user.id.in_(ADMINS))
async def admin(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        SEND_COMMAND,
        reply_markup=AdminKeyboards.admin_menu_inline(),
    )


@admin_router.callback_query(F.data == "promosadmin")
async def promos_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        text=WHATS_NEXT, reply_markup=AdminKeyboards.admin_promos_menu()
    )


@admin_router.callback_query(F.data == "allpromosadmin")
async def get_all_promos(call: types.CallbackQuery, db_session: AsyncSession):
    promo_dal = PromosDAL(db_session)
    all_promos = await promo_dal.get_all_promos()
    if all_promos:
        for promo in all_promos:
            await bot.send_message(
                chat_id=call.from_user.id,
                text=get_promos([promo]),
                reply_markup=AdminKeyboards.get_info_promo_inline(promo.id),
            )
        await bot.send_message(
            call.from_user.id,
            SEND_COMMAND,
            reply_markup=AdminKeyboards.admin_menu_inline(),
        )
    else:
        await bot.send_message(
            call.from_user.id,
            NO_PROMOS,
        )


@admin_router.callback_query(F.data == "addpromos")
async def add_promo_admin(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        call.from_user.id,
        SEND_DESCRIPTION,
        reply_markup=AdminKeyboards.back_to_admin_menu_inline(),
    )
    await state.set_state(FSMAdmin.promo)


@admin_router.callback_query(F.data == "changesettings")
async def change_settings_admin(call: types.CallbackQuery):
    await call.message.edit_text(
        text=WHAT_CHANGE_QUSTION,
        reply_markup=AdminKeyboards.change_settings_admin_inline(),
    )


@admin_router.message(FSMAdmin.promo)
async def get_description_admin(
    message: types.Message, state: FSMContext, db_session: AsyncSession
):
    promo_dal = PromosDAL(db_session)
    new_promo = await promo_dal.add_promo(message.text)
    await bot.send_message(message.from_user.id, get_promos([new_promo]))
    await state.clear()


@admin_router.callback_query(F.data.startswith("removepromo_"))
async def remove_promo(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    promo_dal = PromosDAL(db_session)
    await promo_dal.delete_promo(int(calback_arg))
    await call.message.delete()


@admin_router.callback_query(F.data == "adminback")
async def back_to_menu_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.edit_text(
        text=SEND_COMMAND, reply_markup=AdminKeyboards.admin_menu_inline()
    )


@admin_router.callback_query(
    F.data.startswith("admin_"),
    F.from_user.id.in_(ADMINS),
)
async def get_orders(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    user_id = call.from_user.id
    order_dal = OrderDAL(db_session)
    user_dal = UserDAL(db_session)
    if calback_arg == "active":
        orders = await order_dal.get_all_active_orders()
    else:
        orders = await order_dal.get_completed_orders()
    await call.answer()
    if orders:
        for order in orders:
            user = await user_dal.get_user(order.user_id)
            username = user.username
            await bot.send_message(
                chat_id=user_id,
                text=get_order_for_admin(order, username),
                reply_markup=AdminKeyboards.get_info_order_inline(order.id),
            )
        await bot.send_message(
            call.from_user.id,
            SEND_COMMAND,
            reply_markup=AdminKeyboards.admin_menu_inline(),
        )
    else:
        await bot.send_message(user_id, NO_ORDERS)


@admin_router.callback_query(F.data.startswith("status_"))
async def get_order_status(call: types.CallbackQuery, calback_arg: str):
    await call.message.edit_reply_markup(
        reply_markup=AdminKeyboards.get_status_order_inline(int(calback_arg))
    )


@admin_router.callback_query(F.data.startswith("chstatus_"))
async def change_order_status(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    split_arg = calback_arg.split("_")
    status = split_arg[0]
    order_id = int(split_arg[1])
    order_dal = OrderDAL(db_session)
    user_dal = UserDAL(db_session)

    status_enum = next((s for s in OrderStatus if s.value == status), None)

    if status_enum is None:
        raise ValueError(f"Invalid status: {status}")
    changed_order = await order_dal.update_order(id=order_id, status=status_enum)
    user = await user_dal.get_user(changed_order.user_id)
    username = user.username

    await call.message.edit_text(
        text=get_order_for_admin(changed_order, username),
        reply_markup=AdminKeyboards.get_info_order_inline(changed_order.id),
    )


@admin_router.callback_query(F.data.startswith("removeorder_"))
async def remove_order(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    order_dal = OrderDAL(db_session)
    await order_dal.delete_order(int(calback_arg))
    await call.message.delete()


@admin_router.callback_query(F.data.startswith("backorder_"))
async def back_order(call: types.CallbackQuery, calback_arg: str):
    await call.message.edit_reply_markup(
        reply_markup=AdminKeyboards.get_info_order_inline(int(calback_arg))
    )


@admin_router.callback_query(F.data.startswith("settings_"))
async def get_param_to_settings_admin(
    call: types.CallbackQuery, calback_arg: str, state: FSMContext
):
    await call.answer()
    if calback_arg == "shoes":
        await state.set_state(FSMAdmin.shoes_price)
    elif calback_arg == "cloth":
        await state.set_state(FSMAdmin.cloth_price)
    else:
        await state.set_state(FSMAdmin.current_rate)

    await call.message.edit_text(
        text=SEND_NEW_VALUE, reply_markup=AdminKeyboards.back_to_admin_menu_inline()
    )


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.shoes_price)
async def change_shoes_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="shoes_price", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.cloth_price)
async def change_cloth_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="cloth_price", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.current_rate)
async def change_current_rate(message: types.Message, db_session: AsyncSession):
    try:
        rate = await SettingsDAL(db_session).update_param(
            key="current_rate", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(rate))
    except IndexError:
        await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)
