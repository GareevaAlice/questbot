from aiogram import Dispatcher

from handlers import common, quest_play, quest_create, user


def setup(dp: Dispatcher):
    dp.include_router(quest_play.router)
    dp.include_router(quest_create.router)
    dp.include_router(user.router)
    dp.include_router(common.router)
