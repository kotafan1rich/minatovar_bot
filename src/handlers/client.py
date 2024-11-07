from aiogram import Dispatcher, F, types
from aiogram.filters import Command

from keyboards import cancel_b, get_price_b, get_shoes_price_b, kb_client_main, kb_client_get_price, kb_client_cancel, \
	help_b, get_current_rate_b
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from create_bot import redis_client
from .messages import SEND_PRICE, START, HELP, TYPE_ITEM, send_current_rate_mes, send_price_mes

from create_bot import bot


class FSMGetPrice(StatesGroup):
	get_type_state = State()
	shoes_state = State()
	cloth_state = State()


async def start(message: types.Message):
	await bot.send_message(message.from_user.id, START, reply_markup=kb_client_main)


async def help(message: types.Message):
	await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client_main)


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
	current_state = await state.get_state()
	if current_state is not None:
		await state.clear()
	await message.answer(
		"Отмена",
		reply_markup=kb_client_main,
	)


async def get_type(message: types.Message, state: FSMContext):
	await state.set_state(FSMGetPrice.get_type_state)
	await bot.send_message(message.from_user.id, TYPE_ITEM, reply_markup=kb_client_get_price)


async def set_price_state(message: types.Message, state: FSMContext):
	if message.text == get_shoes_price_b.text:
		media = types.FSInputFile("static/media/shoes_price.jpg")
		await state.set_state(FSMGetPrice.shoes_state)
	else:
		media = types.FSInputFile("static/media/cloth_price.jpg")
		await state.set_state(FSMGetPrice.cloth_state)

	await bot.send_photo(message.from_user.id, photo=media, caption=SEND_PRICE, reply_markup=kb_client_cancel)


async def send_shoes_price(message: types.Message, state: FSMContext):
	await state.clear()
	price = int(message.text)
	delivery_price = int(redis_client.get('shoes_price').decode())
	current_rate = float(redis_client.get('current_rate').decode())
	result_price = round(price * current_rate + delivery_price, 2)

	text = send_price_mes(result_price)
	await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)


async def send_cloth_price(message: types.Message, state: FSMContext):
	await state.clear()
	price = int(message.text)
	delivery_price = int(redis_client.get('cloth_price').decode())
	current_rate = float(redis_client.get('current_rate').decode())
	result_price = round(price * current_rate + delivery_price, 2)

	text = send_price_mes(result_price)
	await bot.send_message(message.from_user.id, text, reply_markup=kb_client_main)


async def get_current_rate(message: types.Message):
	current_rate = str(float(redis_client.get('current_rate').decode()))
	await bot.send_message(message.from_user.id, send_current_rate_mes(current_rate), reply_markup=kb_client_main)


def register_handlers_client(dp: Dispatcher):
	dp.message.register(start, Command("start"))
	dp.message.register(help, F.text == help_b.text)
	dp.message.register(cancel_handler, F.text == cancel_b.text)
	dp.message.register(get_type, F.text == get_price_b.text)
	dp.message.register(get_current_rate, F.text == get_current_rate_b.text)
	dp.message.register(set_price_state, FSMGetPrice.get_type_state)
	dp.message.register(send_shoes_price, FSMGetPrice.shoes_state)
	dp.message.register(send_cloth_price, FSMGetPrice.cloth_state)
