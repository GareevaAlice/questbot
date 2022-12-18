from aiogram import Dispatcher

from handlers import common, menu, create_quest, quest, delete_quest, quests_list, play_quest


def setup(dp: Dispatcher):
    dp.include_router(play_quest.router)
    dp.include_router(quests_list.router)
    dp.include_router(delete_quest.router)
    dp.include_router(quest.router)
    dp.include_router(create_quest.router)
    dp.include_router(menu.router)
    dp.include_router(common.router)
