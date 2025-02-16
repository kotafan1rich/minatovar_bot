from typing import List

from db.models import Order, Promos

HELP = "Если у вас есть вопросы по доставке, ценообразованию и качеству товара, то \
можете написать нашему администратору\n\nКанал: @MINATOVARSHOP\nАдминистратор: @UglyMJoy"

START = "Здравствуйте, этот бот поможет вам рассчитать стоимость желанного товара…"

SEND_PRICE = (
    "Отправьте число, которое у вас указано на бирюзовой кнопке…\n\nПрисылайте \
число без учета скидки Poizon"
)

TYPE_ITEM = "Выберите тип товара"

BAD_FORMAT_ERROR = "Неправильный формат ввода"
NON_ARGUMENT_ERROR = "Не введён аргумент"
BOT_IS_UNVAILABLE = "Бот в данный момент недоступен. Приносим свои изменения"
UNCORRECT_URL = "Некорректная ссылка"
SET_USERNAME = "Установите username и повторите попытку"
NO_PROMOS = "Нет акций"
NOT_DIGIT_ERROR = "Введите целое число"


SEND_COMMAND = "Отпарвьте команду"
WHAT_CHANGE_QUSTION = "Что хотите поменять?"
NO_ORDERS = "Нет заказов"
SEND_NEW_VALUE = "Отправьте новое значение"
SEND_DESCRIPTION = "Отправьте описание акции"

MAIN_MENU = "Выберите нужный раздел, чтобы начать работу с ботом."
WHATS_NEXT = "Что вы хотите сделать дальше?"
USERS_NO_ORDERS = "У вас нет заказов"
SEND_ARTICLE = "Отпрвьте артикул товара"
SEND_ADDRES = "Укажите, в каком формате удобнее:\n\n\
<b>Для отправки через СДЭК:</b>\nУточните полный адрес пункта выдачи.\n\n\
<b>Для личной встречи (СПБ):</b> Заберу заказ лично."
SEND_SIZE = "Укажите размер, ровно так же как в приложении"
ADDED = "Добавлено"


def send_price_mes(price) -> str:
    return f"Итог: {price}₽\n\nПара прибывает в Москву (19-26 дней)\n\nДополнительно \
оплачивается доставка СДЭК до вашего города. Если вы живете в Питере, то \
доставка будет стоить 500₽ до склада в СПБ\n\n•Не забывайте, что много \
интересных вещей уже есть в нашем магазине 🤙"


def send_current_rate_mes(current_rate: float) -> str:
    return f"💵 Курс валюты:\nЮань (CNY): {current_rate}₽"


def refferal_link(bot_username, user_id) -> str:
    return f"📢 Поделитесь своей реферальной ссылкой:\n\
https://t.me/{bot_username}?start={user_id}\n\
Приглашайте друзей и получайте бонусы!"


def count_referrals(refs: list, actives: int):
    return f"📈 Мои рефералы:\nОбщее количество: {len(refs)}\nАктивных \
(покупки больше 5000₽): {actives}"


def confrim_order(order: Order):
    return f"""
<b>Проверьте</b>:

<b>Артикул:</b> {order.article}
<b>Размер:</b> {order.size}
<b>Тип:</b> {order.type_item}
<b>Цена (RUB):</b> {order.price_rub}₽
<b>Цена (CNY):</b> {order.price_cny}¥
<b>Адрес:</b> {order.addres}
"""


def get_order_for_admin(order: Order, username: str):
    return f"""
<b>ID заказа:</b> {order.id}
<b>Статус:</b> {order.status.value}
<b>Артикул:</b> {order.article}
<b>Размер:</b> {order.size}
<b>Тип:</b> {order.type_item.value}
<b>Цена (RUB):</b> {order.price_rub}₽
<b>Цена (CNY):</b> {order.price_cny}¥
<b>Адрес:</b> {order.addres}
<b>Пользователь:</b> @{username}
<b>Дата создания:</b> {order.time_created.strftime("%d.%m.%Y %H:%M:%S MSK")}
"""


def get_new_order_for_admin(order: Order, username: str):
    return f"""
<b>!!!НОВЫЙ ЗАКАЗ!!!</b>

<b>ID заказа:</b> {order.id}
<b>Статус:</b> {order.status.value}
<b>Артикул:</b> {order.article}
<b>Размер:</b> {order.size}
<b>Тип:</b> {order.type_item.value}
<b>Цена (RUB):</b> {order.price_rub}₽
<b>Цена (CNY):</b> {order.price_cny}¥
<b>Адрес:</b> {order.addres}
<b>Пользователь:</b> @{username}
<b>Дата создания:</b> {order.time_created.strftime("%d.%m.%Y %H:%M:%S MSK")}
"""


def get_order(order: Order) -> str:
    return f"""
<b>Детали заказа:</b>

<b>ID заказа:</b> {order.id}
<b>Статус:</b> {order.status.value}
<b>Артикул:</b> {order.article}
<b>Размер:</b> {order.size}
<b>Тип:</b> {order.type_item.value}
<b>Цена (RUB):</b> {order.price_rub}₽
<b>Цена (CNY):</b> {order.price_cny}¥
<b>Адрес:</b> {order.addres}
<b>Дата создания:</b> {order.time_created.strftime("%d.%m.%Y")}
"""


def get_promos(promos: List[Promos]):
    return "".join(f"{promo.descriptions}\n\n" for promo in promos)
