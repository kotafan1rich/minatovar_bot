from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from config import STATIC_FILES
from create_bot import bot
from db.dals import OrderDAL, UserDAL
from db.models import Order, OrderTypeItem
from fsms import FSMOrder
from keyboards import ClientKeyboards, OrderKeyboards
from sqlalchemy.ext.asyncio import AsyncSession
from utils.orders import calculate_rub_price


from .messages import (
    MAIN_MENU,
    SEND_ADDRES,
    SEND_ARTICLE,
    SEND_PRICE,
    SEND_SIZE,
    SET_USERNAME,
    TYPE_ITEM,
    USERS_NO_ORDERS,
    WHATS_NEXT,
    confrim_order,
    get_new_order_for_admin,
    get_order,
)

order_roter = Router(name="order_handler")


@order_roter.callback_query(F.data.startswith("orders"))
async def order_menu(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=WHATS_NEXT,
        reply_markup=OrderKeyboards.order_menu_inline(),
    )


@order_roter.callback_query(F.data == "backtoorders")
async def back_to_orders(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=WHATS_NEXT,
        reply_markup=OrderKeyboards.order_menu_inline(),
    )


@order_roter.callback_query(F.data.startswith("myorders"))
async def get_my_orders(call: types.CallbackQuery, db_session: AsyncSession):
    user_id = call.from_user.id
    order_dal = OrderDAL(db_session)
    orders = await order_dal.get_orders_for_user(user_id)
    if orders:
        await call.answer()
        for order in orders:
            await bot.send_message(user_id, get_order(order))
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=USERS_NO_ORDERS,
            reply_markup=OrderKeyboards.order_menu_inline(),
        )


@order_roter.callback_query(F.data.startswith("createorder"))
async def create_order(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.answer()
    if call.from_user.username:
        await bot.send_message(
            user_id,
            SEND_ARTICLE,
            reply_markup=OrderKeyboards.close_inline(),
        )
        await state.set_state(FSMOrder.article)
    else:
        await bot.send_message(
            user_id,
            SET_USERNAME,
            reply_markup=OrderKeyboards.back_to_orders_inline(),
        )


@order_roter.message(FSMOrder.article)
async def get_article(messgae: types.Message, state: FSMContext):
    article = messgae.text
    user_id = messgae.from_user.id
    # if is_valid_link(url):
    await state.update_data(article=article)
    await bot.send_message(
        user_id,
        TYPE_ITEM,
        reply_markup=OrderKeyboards.get_type_item_inline(),
    )
    await state.set_state(FSMOrder.type_item)
    # else:
    #     await bot.send_message(
    #         user_id,
    #         UNCORRECT_URL,
    #         reply_markup=OrderKeyboards.back_to_orders_inline(),
    #     )


@order_roter.callback_query(FSMOrder.type_item, F.data.startswith("type_"))
async def get_type_item(call: types.CallbackQuery, calback_arg: str, state: FSMContext):
    await state.update_data(type_item=calback_arg)
    await state.set_state(FSMOrder.addres)
    await call.answer()
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=SEND_ADDRES,
        reply_markup=OrderKeyboards.back_to_orders_inline(),
    )


@order_roter.message(FSMOrder.addres)
async def get_addres(messgae: types.Message, state: FSMContext):
    addres = messgae.text
    await state.update_data(addres=addres)
    data = await state.get_data()
    type_item = data["type_item"]
    if type_item == OrderTypeItem.SHOES.value:
        media_group = [
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/shoes_price_2.jpg")
            ),
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/shoes_price.jpg"),
                caption=SEND_PRICE,
            ),
        ]
    else:
        media_group = [
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/cloth_price_2.jpg")
            ),
            types.InputMediaPhoto(
                media=types.FSInputFile(f"{STATIC_FILES}/cloth_price.jpg"),
                caption=SEND_PRICE,
            ),
        ]
    await bot.send_media_group(messgae.from_user.id, media=media_group)
    await state.set_state(FSMOrder.price_cny)


@order_roter.message(FSMOrder.price_cny)
async def get_prcie(messgae: types.Message, state: FSMContext):
    price = int(messgae.text)
    await state.update_data(price_cny=price)
    await bot.send_message(
        messgae.from_user.id,
        SEND_SIZE,
        reply_markup=OrderKeyboards.close_inline(),
    )
    await state.set_state(FSMOrder.size)


@order_roter.message(FSMOrder.size)
async def get_size(messgae: types.Message, state: FSMContext, db_session: AsyncSession):
    user_id = messgae.from_user.id
    size = messgae.text.replace(",", ".")
    size = float(size)
    await state.update_data(size=size)
    data = await state.get_data()
    res_price_rub = await calculate_rub_price(
        user_id=user_id,
        price_cny=data["price_cny"],
        type_item=data["type_item"],
        db_session=db_session,
    )

    data["price_rub"] = res_price_rub
    await state.set_data(data)
    order = confrim_order(Order(**data))
    await bot.send_message(user_id, order, reply_markup=OrderKeyboards.confrim_inline())
    await state.set_state(FSMOrder.confrim)


@order_roter.callback_query(FSMOrder.confrim, F.data.startswith("confrim"))
async def confrim(
    call: types.CallbackQuery, state: FSMContext, db_session: AsyncSession
):
    user_id = call.from_user.id
    username = call.from_user.username

    user_dal = UserDAL(db_session)
    order_dal = OrderDAL(db_session)
    data = await state.get_data()
    if data["type_item"] == OrderTypeItem.SHOES.value:
        data["type_item"] = OrderTypeItem.SHOES
    else:
        data["type_item"] = OrderTypeItem.CLOTH
    await user_dal.update_user(user_id=user_id, username=username)
    created_order = await order_dal.add_order(user_id=user_id, **data)

    await call.answer()
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=get_order(created_order),
    )
    await state.clear()
    await bot.send_message(
        user_id, MAIN_MENU, reply_markup=ClientKeyboards.main_menu_inline_kb()
    )


    await bot.send_message(
        chat_id="-1002174701809", text=get_new_order_for_admin(created_order, username)
    )
