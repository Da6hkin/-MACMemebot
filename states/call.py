from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeCall(StatesGroup):
    YesOrNo = State()
