from db.models import Order

HELP = "Если у вас есть вопросы по доставке, ценообразованию и качеству товара, то\
можете написать нашему администратору\n\nАдминистратор: @UglyMJoy"

START = "Здравствуйте, этот бот поможет вам рассчитать стоимость желанного товара…"

SEND_PRICE = (
    "Отправьте число, которое у вас указано на бирюзовой кнопке…\n\nПрисылайте \
число без учета скидки Poizon"
)

TYPE_ITEM = "Обувь/Одежда"

ADMIN_HELP = (
    "/adminhelp\n/shoes число (доставка)\n/cloth число (доставка)\n/rate число (курс)"
)

BAD_FORMAT_ERROR = "Неправильный формат ввода"
NON_ARGUMENT_ERROR = "Не введён аргумент"
BOT_IS_UNVAILABLE = "Бот в данный момент недоступен. Приносим свои изменения"
UNCORRECT_URL = "Некорректная ссылка"
SET_USERNAME = "Установите username и повторите попытку"


SEND_COMMAND = "Отпарвьте команду"
WHAT_CHANGE_QUSTION = "Что хотите поменять?"
NO_ORDERS = "Нет заказов"
SEND_NEW_VALUE = "Отправьте новое значение"

MAIN_MENU = "Главное меню"
WHATS_NEXT = "Что дальше?"
USERS_NO_ORDERS = "У вас нет заказов"
SEND_URL = "Отпрвьте url товара"
SEND_ADDRES = "Отправьте адрес"
SEND_SIZE = "Отправьте размер"


def send_price_mes(price) -> str:
    return f"Итог: {price}₽\n\nПара прибывает в Москву (19-26 дней)\n\nДополнительно \
оплачивается доставка СДЭК до вашего города. Если вы живете в Питере, то \
доставка будет стоить 500₽ до склада в СПБ\n\n•Не забывайте, что много \
интересных вещей уже есть в нашем магазине 🤙"


def send_current_rate_mes(current_rate) -> str:
    return f"1¥ = {current_rate}₽"


def refferal_link(bot_username, user_id) -> str:
    return f"https://t.me/{bot_username}?start={user_id}"


def count_referrals(refs: list):
    return f"Количество ваших рефералов: {len(refs)}"


def confrim_order(order: Order):
    return f"""Проверьте:
Ссылка: {order.url}
Размер: {order.size}
Тип: {order.type_item}
Цена (RUB): {order.price_rub}₽
Цена (CNY): {order.price_cny}¥
Адрес: {order.addres}
"""


def get_order_for_admin(order: Order, username: str):
    return f"""ID заказа: {order.id}
Статус: {order.status.value}
Ссылка: {order.url}
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
Ссылка: {order.url}
Размер: {order.size}
Тип: {order.type_item.value}
Цена (RUB): {order.price_rub}₽
Цена (CNY): {order.price_cny}¥
Адрес: {order.addres}
Дата создания: {order.time_created.strftime("%d.%m.%Y MSK")}
"""
