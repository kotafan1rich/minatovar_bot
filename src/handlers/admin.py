from aiogram import Dispatcher, types
from aiogram.filters import Command

from .messages import BAD_FORMAT_ERROR, NON_ARGUMENT_ERROR, ADMIN_HELP

from create_bot import bot, redis_client

admins = [1019030670, 1324716819]


async def change_shoes_price(message: types.Message):
	if message.from_user.id in admins:
		try: 
			price = int(message.text.split(" ")[1])
			redis_client.set("shoes_price", price)
			await bot.send_message(message.from_user.id, str(price))
		except IndexError:
			await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
		except ValueError:
			await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


async def change_cloth_price(message: types.Message):
	if message.from_user.id in admins:
		try:
			price = int(message.text.split(" ")[1])
			redis_client.set("cloth_price", price)
			await bot.send_message(message.from_user.id, str(price))
		except IndexError:
			await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
		except ValueError:
			await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


async def change_current_rate(message: types.Message):
	if message.from_user.id in admins:
		try:
			rate = float(message.text.split(" ")[1])
			redis_client.set("current_rate", rate)
			await bot.send_message(message.from_user.id, str(rate))
		except IndexError:
			await bot.send_message(message.from_user.id, NON_ARGUMENT_ERROR)
		except ValueError:
			await bot.send_message(message.from_user.id, BAD_FORMAT_ERROR)


async def admin_help(message: types.Message):
	if message.from_user.id in admins:
		await bot.send_message(message.from_user.id, ADMIN_HELP)


def register_handlers_admin(dp: Dispatcher):
	dp.message.register(change_shoes_price, Command("shoes"))
	dp.message.register(change_cloth_price, Command("cloth"))
	dp.message.register(change_current_rate, Command("rate"))
	dp.message.register(admin_help, Command("adminhelp"))
