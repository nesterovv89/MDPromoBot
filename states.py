from aiogram.fsm.state import State, StatesGroup


class Pool(StatesGroup):
    what = State()
    custom_option = State()
    age = State()
    wish = State()


class ToState(StatesGroup):
    name = State()
    age = State()
    #method = State()
    comment = State()
