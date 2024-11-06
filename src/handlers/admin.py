from aiogram import Dispatcher, types
from aiogram.filters import Command

from create_bot import bot, redis_client

admins = [1019030670, 1324716819]


async def change_shoes_price(message: types.Message):
	if message.from_user.id in admins:
		price = int(message.text.split(" ")[1])
		redis_client.set("shoes_price", price)
		await bot.send_message(message.from_user.id, str(price))


async def change_cloth_price(message: types.Message):
	if message.from_user.id in admins:
		price = int(message.text.split(" ")[1])
		redis_client.set("cloth_price", price)
		await bot.send_message(message.from_user.id, str(price))


async def change_current_rate(message: types.Message):
	if message.from_user.id in admins:
		rate = float(message.text.split(" ")[1])
		redis_client.set("current_rate", rate)
		await bot.send_message(message.from_user.id, str(rate))


async def admin_help(message: types.Message):
	if message.from_user.id in admins:
		await bot.send_message(message.from_user.id, "/adminhelp\n/shoes число (доставка)\n/cloth число (доставка)\n/rate число (курс)")


def register_handlers_admin(dp: Dispatcher):
	dp.message.register(change_shoes_price, Command("shoes"))
	dp.message.register(change_cloth_price, Command("cloth"))
	dp.message.register(change_current_rate, Command("rate"))
	dp.message.register(admin_help, Command("adminhelp"))
