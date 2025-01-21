from typing import List

from db.models import Order, Promos

HELP = "Если у вас есть вопросы по доставке, ценообразованию и качеству товара, то\
можете написать нашему администратору\n\nАдминистратор: @UglyMJoy"

START = "Здравствуйте, этот бот поможет вам рассчитать стоимость желанного товара…"

SEND_PRICE = (
    "Отправьте число, которое у вас указано на бирюзовой кнопке…\n\nПрисылайте \
число без учета скидки Poizon"
)

TYPE_ITEM = "Обувь/Одежда"

BAD_FORMAT_ERROR = "Неправильный формат ввода"
NON_ARGUMENT_ERROR = "Не введён аргумент"
BOT_IS_UNVAILABLE = "Бот в данный момент недоступен. Приносим свои изменения"
UNCORRECT_URL = "Некорректная ссылка"
SET_USERNAME = "Установите username и повторите попытку"
NO_PROMOS = "Нет акций"


SEND_COMMAND = "Отпарвьте команду"
WHAT_CHANGE_QUSTION = "Что хотите поменять?"
NO_ORDERS = "Нет заказов"
SEND_NEW_VALUE = "Отправьте новое значение"
SEND_DESCRIPTION = "Отправьте описание акции"

MAIN_MENU = "Выберите нужный раздел, чтобы начать работу с ботом."
WHATS_NEXT = "Что вы хотите сделать дальше?"
USERS_NO_ORDERS = "У вас нет заказов"
SEND_ARTICLE = "Отпрвьте артикул товара"
SEND_ADDRES = "Отправьте адрес"
SEND_SIZE = "Отправьте размер"
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
    return f"""Проверьте:
Артикул: {order.article}
Размер: {order.size}
Тип: {order.type_item}
Цена (RUB): {order.price_rub}₽
Цена (CNY): {order.price_cny}¥
Адрес: {order.addres}
"""


def get_order_for_admin(order: Order, username: str):
    return f"""ID заказа: {order.id}
Статус: {order.status.value}
Артикул: {order.article}
Размер: {order.size}
Тип: {order.type_item.value}
Цена (RUB): {order.price_rub}₽
Цена (CNY): {order.price_cny}¥
Адрес: {order.addres}
Пользователь: @{username}
Дата создания: {order.time_created.strftime("%d.%m.%Y %H:%M:%S MSK")}
"""


def get_order(order: Order):
    return f"""ID заказа: {order.id}
Статус: {order.status.value}
Артикул: {order.article}
Размер: {order.size}
Тип: {order.type_item.value}
Цена (RUB): {order.price_rub}₽
Цена (CNY): {order.price_cny}¥
Адрес: {order.addres}
Дата создания: {order.time_created.strftime("%d.%m.%Y")}
"""


def get_promos(promos: List[Promos]):
    return "".join(f"{promo.descriptions}\n\n" for promo in promos)
