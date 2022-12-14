from aiogram.dispatcher.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    playing_quest = State()
    getting_quest_xml = State()
