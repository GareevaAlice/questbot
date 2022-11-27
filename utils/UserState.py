from aiogram.dispatcher.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    getting_quest_info = State()
    playing_quest = State()
    getting_quest_xml = State()
