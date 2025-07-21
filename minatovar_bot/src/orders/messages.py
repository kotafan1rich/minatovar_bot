from src.messages import MessageBase
from src.orders.models import Order


class MessageOrders(MessageBase):
    USERS_NO_ORDERS = "У вас нет заказов"
    SEND_ARTICLE = "Отпрвьте артикул товара"
    SEND_ADDRES = "Укажите, в каком формате удобнее:\n\n\
<b>Для отправки через СДЭК:</b>\nУточните полный адрес пункта выдачи.\n\n\
<b>Для личной встречи (СПБ):</b> Заберу заказ лично."
    SEND_SIZE = "Укажите размер, ровно так же как в приложении"
    ADDED = "Добавлено"
    SET_USERNAME = (
        "Установите username, чтобы могли с вами связаться после оформления закза."
    )

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
