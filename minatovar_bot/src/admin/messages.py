from src.orders.models import Order
from src.messages import MessageBase


class MessageAdmin(MessageBase):
    SEND_DESCRIPTION = "Отправьте описание акции"
    SEND_NEW_VALUE = "Отправьте новое значение"
    WHAT_CHANGE_QUSTION = "Что хотите поменять?"
    BAD_FORMAT_ERROR = "Неправильный формат ввода"
    NON_ARGUMENT_ERROR = "Не введён аргумент"
    SEND_COMMAND = "Отпарвьте команду"
    NO_ORDERS = "Нет заказов"

    @staticmethod
    def get_order_for_admin(order: Order, username: str) -> str:
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
