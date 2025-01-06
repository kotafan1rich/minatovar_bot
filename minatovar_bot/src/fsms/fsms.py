from aiogram.fsm.state import State, StatesGroup


class FSMOrder(StatesGroup):
    url = State()
    type_item = State()
    addres = State()
    price_cny = State()
    size = State()
    confrim = State()


class FSMGetPrice(StatesGroup):
    get_type_state = State()
    shoes_state = State()
    cloth_state = State()


class FSMChangeSettings(StatesGroup):
    shoes_price = State()
    cloth_price = State()
    current_rate = State()
