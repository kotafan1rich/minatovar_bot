from src.messages import MessageBase


class MessageClient(MessageBase):
    HELP = (
        "Если у вас есть вопросы по доставке, ценообразованию или качеству товара, то \
можете написать нашему администратору\n\nКанал: \
@MINATOVARSHOP\nАдминистратор: @UglyMJoy"
    )

    START = "Здравствуйте, этот бот поможет вам рассчитать стоимость желанного товара…"

    SEND_PRICE = (
        "Отправьте число, которое у вас указано на бирюзовой кнопке…\n\nПрисылайте \
число без учета скидки Poizon"
    )
    U_ARE_REFERRAL = "🎉 Поздравляем! Теперь вы – реферал."
    NEW_REFERRAL = "🙌 Отлично! У вас новый реферал."

    @staticmethod
    def send_current_rate_mes(current_rate: float) -> str:
        return f"💵 Курс валюты:\nЮань (CNY): {current_rate}₽"

    @staticmethod
    def refferal_link(bot_username, user_id) -> str:
        return f"📢 Поделитесь своей реферальной ссылкой:\n\
https://t.me/{bot_username}?start={user_id}\n\
Приглашайте друзей и получайте бонусы!"

    @staticmethod
    def count_referrals(refs: list, actives: int) -> str:
        return f"📈 Мои рефералы:\nОбщее количество: {len(refs)}\nАктивных \
(покупки больше 5000₽): {actives}"

    @staticmethod
    def send_price_mes(price) -> str:
        return (
            f"Итог: {price}₽\n\nТовар прибывает в Москву (19-26 дней)\n\nДополнительно \
оплачивается доставка СДЭК до вашего города. Если вы живете в Питере, то \
доставка будет стоить 500₽ до склада в СПБ\n\n•Не забывайте, что много \
интересных вещей уже есть в нашем магазине 🤙"
        )
