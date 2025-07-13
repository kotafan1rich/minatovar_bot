from typing import Optional

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.create_bot import bot
from src.db.dals import PromosDAL, ReferralDAL, SettingsDAL
from src.db.models import OrderTypeItem
from src.fsms import FSMGetPrice
from src.keyboards import ClientKeyboards
from src.utils.meida import get_media_group_cloth, get_media_group_shoes
from src.utils.orders import calculate_rub_price, get_active_referrals

from .messages import (
    BOT_IS_UNVAILABLE,
    HELP,
    MAIN_MENU,
    NEW_REFERRAL,
    NO_PROMOS,
    NOT_DIGIT_ERROR,
    START,
    TYPE_ITEM,
    U_ARE_REFERRAL,
    WHATS_NEXT,
    count_referrals,
    get_promos,
    refferal_link,
    send_current_rate_mes,
    send_price_mes,
)

client_router = Router(name="client_router")


@client_router.message(Command("start"), flags={"start": True})
async def start(message: types.Message, state: FSMContext, referrer_id: Optional[int]):
    user_id = message.from_user.id
    if referrer_id:
        await bot.send_message(referrer_id, NEW_REFERRAL)
        await bot.send_message(user_id, U_ARE_REFERRAL)

    await bot.send_message(user_id, START, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(
        user_id,
        MAIN_MENU,
        reply_markup=ClientKeyboards.main_menu_inline_kb(),
    )
    await state.clear()


@client_router.callback_query(F.data.startswith("close"))
async def close(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()


@client_router.callback_query(F.data == "back")
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        text=MAIN_MENU, reply_markup=ClientKeyboards.main_menu_inline_kb()
    )


@client_router.callback_query(F.data == "help")
async def help(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(
        call.from_user.id, HELP, reply_markup=ClientKeyboards.close_inline()
    )


@client_router.callback_query(F.data == "promosclient")
async def promos(call: types.CallbackQuery, db_session: AsyncSession):
    await call.answer()
    promos_dal = PromosDAL(db_session)
    all_promos = await promos_dal.get_all_promos()
    if all_promos:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=get_promos(all_promos),
            reply_markup=ClientKeyboards.close_inline(),
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=NO_PROMOS,
            reply_markup=ClientKeyboards.close_inline(),
        )


@client_router.callback_query(F.data == "getprice")
async def get_type(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMGetPrice.get_type_state)
    await call.answer()
    await bot.send_message(
        chat_id=call.from_user.id,
        text=TYPE_ITEM,
        reply_markup=ClientKeyboards.get_type_item_inline(),
    )


@client_router.callback_query(FSMGetPrice.get_type_state, F.data.startswith("type_"))
async def set_price_state(
    call: types.CallbackQuery, state: FSMContext, calback_arg: str
):
    await call.message.delete()
    if calback_arg == OrderTypeItem.SHOES.value:
        media_group = get_media_group_shoes()
        await state.set_state(FSMGetPrice.shoes_state)
    else:
        media_group = get_media_group_cloth()
        await state.set_state(FSMGetPrice.cloth_state)
    await call.answer()
    await bot.send_media_group(call.from_user.id, media=media_group)


@client_router.message(FSMGetPrice.shoes_state)
async def send_shoes_price(message: types.Message, state: FSMContext, db_session):
    user_id = message.from_user.id
    if message.text and message.text.isdigit() and int(message.text) > 0:
        price = int(message.text)
        delivery_price = await SettingsDAL(db_session).get_param("shoes_price")
        current_rate = await SettingsDAL(db_session).get_param("current_rate")
        if delivery_price and current_rate:
            res_price_rub = await calculate_rub_price(
                user_id=user_id,
                price_cny=price,
                type_item=OrderTypeItem.SHOES,
                db_session=db_session,
            )

            text = send_price_mes(res_price_rub)
            await bot.send_message(user_id, text)
        else:
            await bot.send_message(user_id, BOT_IS_UNVAILABLE)
        await bot.send_message(
            chat_id=user_id,
            text=MAIN_MENU,
            reply_markup=ClientKeyboards.main_menu_inline_kb(),
        )
        await state.clear()
    else:
        await bot.send_message(user_id, NOT_DIGIT_ERROR)


@client_router.message(FSMGetPrice.cloth_state)
async def send_cloth_price(message: types.Message, state: FSMContext, db_session):
    user_id = message.from_user.id
    if message.text and message.text.isdigit() and int(message.text) > 0:
        price = int(message.text)
        delivery_price = await SettingsDAL(db_session).get_param("cloth_price")
        current_rate = await SettingsDAL(db_session).get_param("current_rate")
        if delivery_price and current_rate:
            res_price_rub = await calculate_rub_price(
                user_id=user_id,
                price_cny=price,
                type_item=OrderTypeItem.CLOTH,
                db_session=db_session,
            )

            text = send_price_mes(res_price_rub)
            await bot.send_message(user_id, text)
        else:
            await bot.send_message(user_id, BOT_IS_UNVAILABLE)
        await bot.send_message(
            chat_id=user_id,
            text=MAIN_MENU,
            reply_markup=ClientKeyboards.main_menu_inline_kb(),
        )
        await state.clear()
    else:
        await bot.send_message(user_id, NOT_DIGIT_ERROR)


@client_router.callback_query(F.data == "getrate")
async def get_current_rate(call: types.CallbackQuery, db_session):
    await call.answer()
    if current_rate := await SettingsDAL(db_session).get_param("current_rate"):
        await bot.send_message(
            call.from_user.id,
            send_current_rate_mes(current_rate),
            reply_markup=ClientKeyboards.close_inline(),
        )
    else:
        await bot.send_message(
            call.from_user.id,
            BOT_IS_UNVAILABLE,
            reply_markup=ClientKeyboards.main_menu_inline_kb(),
        )


@client_router.callback_query(F.data == "referralmenu")
async def referral_menu(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(
        chat_id=call.from_user.id,
        text=WHATS_NEXT,
        reply_markup=ClientKeyboards.get_referral_menu_inline(),
    )


@client_router.callback_query(F.data == "referralurl")
async def get_refferal_link(call: types.CallbackQuery):
    info_bot = await bot.get_me()
    await call.message.edit_text(
        text=refferal_link(bot_username=info_bot.username, user_id=call.from_user.id),
        reply_markup=ClientKeyboards.close_inline(),
    )


@client_router.callback_query(F.data == "myreferrals")
async def get_my_referrals(call: types.CallbackQuery, db_session: AsyncSession):
    user_id = call.from_user.id
    referral_dal = ReferralDAL(db_session)

    referrals = await referral_dal.get_refferals(int(call.from_user.id))
    actives = await get_active_referrals(
        user_id=user_id, user_referrals=referrals, db_session=db_session
    )
    await call.message.edit_text(
        text=count_referrals(referrals, actives),
        reply_markup=ClientKeyboards.close_inline(),
    )
