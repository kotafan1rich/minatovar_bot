
from src.admin.models import Promos


class MessageBase:
    TYPE_ITEM = "Выберите тип товара"

    BOT_IS_UNVAILABLE = "Бот в данный момент недоступен. Приносим свои изменения"
    NO_PROMOS = "Нет акций"
    NOT_DIGIT_ERROR = "Введите целое число"

    WHATS_NEXT = "Что вы хотите сделать дальше?"

    MAIN_MENU = "Выберите нужный раздел, чтобы начать работу с ботом."
    @staticmethod
    def get_promos(promos: list[Promos]) -> str:
        return "".join(f"{promo.descriptions}\n\n" for promo in promos)

