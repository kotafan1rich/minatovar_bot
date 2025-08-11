from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.admin.dal import PromosDAL, SettingsDAL
from src.admin.keyboards import AdminKeyboards
from src.admin.messages import MessageAdmin
from src.client.dal import UserDAL
from src.config import ADMINS
from src.create_bot import bot
from src.fsms import FSMAdmin

from src.orders.dal import OrderDAL
from src.orders.models import OrderStatus

admin_router = Router(name="admin_router")


@admin_router.message(Command("admin"), F.from_user.id.in_(ADMINS))
async def admin(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        MessageAdmin.SEND_COMMAND,
        reply_markup=AdminKeyboards.admin_menu_inline(),
    )


@admin_router.callback_query(F.data == "promosadmin")
async def promos_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        text=MessageAdmin.WHATS_NEXT, reply_markup=AdminKeyboards.admin_promos_menu()
    )


@admin_router.callback_query(F.data == "allpromosadmin")
async def get_all_promos(call: types.CallbackQuery, db_session: AsyncSession):
    promo_dal = PromosDAL(db_session)
    all_promos = await promo_dal.get_all_promos()
    await call.answer()
    if all_promos:
        for promo in all_promos:
            await bot.send_message(
                chat_id=call.from_user.id,
                text=MessageAdmin.get_promos([promo]),
                reply_markup=AdminKeyboards.get_info_promo_inline(promo.id),
            )
        await bot.send_message(
            call.from_user.id,
            MessageAdmin.SEND_COMMAND,
            reply_markup=AdminKeyboards.admin_menu_inline(),
        )
    else:
        await bot.send_message(
            call.from_user.id,
            MessageAdmin.NO_PROMOS,
        )


@admin_router.callback_query(F.data == "addpromos")
async def add_promo_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.send_message(
        call.from_user.id,
        MessageAdmin.SEND_DESCRIPTION,
        reply_markup=AdminKeyboards.back_to_admin_menu_inline(),
    )
    await state.set_state(FSMAdmin.promo)


@admin_router.callback_query(F.data == "changesettings")
async def change_settings_admin(call: types.CallbackQuery):
    await call.message.edit_text(
        text=MessageAdmin.WHAT_CHANGE_QUSTION,
        reply_markup=AdminKeyboards.change_settings_admin_inline(),
    )


@admin_router.message(FSMAdmin.promo)
async def get_description_admin(
    message: types.Message, state: FSMContext, db_session: AsyncSession
):
    promo_dal = PromosDAL(db_session)
    new_promo = await promo_dal.add_promo(message.text)
    await bot.send_message(message.from_user.id, MessageAdmin.get_promos([new_promo]))
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
        text=MessageAdmin.SEND_COMMAND, reply_markup=AdminKeyboards.admin_menu_inline()
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
                text=MessageAdmin.get_order_for_admin(order, username),
                reply_markup=AdminKeyboards.get_info_order_inline(order.id),
            )
        await bot.send_message(
            call.from_user.id,
            MessageAdmin.SEND_COMMAND,
            reply_markup=AdminKeyboards.admin_menu_inline(),
        )
    else:
        await bot.send_message(user_id, MessageAdmin.NO_ORDERS)


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

    status_enum = next((s for s in OrderStatus if s.display() == status), None)

    if status_enum is None:
        raise ValueError(f"Invalid status: {status}")
    changed_order = await order_dal.update_order(id=order_id, status=status_enum)
    user = await user_dal.get_user(changed_order.user_id)
    username = user.username

    await call.message.edit_text(
        text=MessageAdmin.get_order_for_admin(changed_order, username),
        reply_markup=AdminKeyboards.get_info_order_inline(changed_order.id),
    )


@admin_router.callback_query(F.data.startswith("removeorder_"))
async def remove_order(
    call: types.CallbackQuery, calback_arg: str, db_session: AsyncSession
):
    await call.message.edit_reply_markup(
        reply_markup=AdminKeyboards.get_confrim_delete_order_inline(int(calback_arg)),
    )


@admin_router.callback_query(F.data.startswith("confrimremoveorder_"))
async def confrim_remove_order(
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
        text=MessageAdmin.SEND_NEW_VALUE,
        reply_markup=AdminKeyboards.back_to_admin_menu_inline(),
    )


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.shoes_price)
async def change_shoes_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="shoes_price", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, MessageAdmin.NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, MessageAdmin.BAD_FORMAT_ERROR)


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.cloth_price)
async def change_cloth_price(message: types.Message, db_session: AsyncSession):
    try:
        price = await SettingsDAL(db_session).update_param(
            key="cloth_price", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(price))
    except IndexError:
        await bot.send_message(message.from_user.id, MessageAdmin.NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, MessageAdmin.BAD_FORMAT_ERROR)


@admin_router.message(F.from_user.id.in_(ADMINS), FSMAdmin.current_rate)
async def change_current_rate(message: types.Message, db_session: AsyncSession):
    try:
        rate = await SettingsDAL(db_session).update_param(
            key="current_rate", value=float(message.text.replace(",", "."))
        )
        await bot.send_message(message.from_user.id, str(rate))
    except IndexError:
        await bot.send_message(message.from_user.id, MessageAdmin.NON_ARGUMENT_ERROR)
    except ValueError:
        await bot.send_message(message.from_user.id, MessageAdmin.BAD_FORMAT_ERROR)
