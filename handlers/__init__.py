from aiogram import Dispatcher

from handlers import common, play_quest, create_quest, user


def setup(dp: Dispatcher):
    dp.include_router(play_quest.router)
    dp.include_router(create_quest.router)
    dp.include_router(user.router)
    dp.include_router(common.router)
