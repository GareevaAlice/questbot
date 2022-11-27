import json

from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.types import Message

from utils.DBManager import db_manager

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


@router.message(Command(commands=["user_info"]))
async def user_info(message: Message):
    await message.answer(
        text=temp_text['user_info'].format(
            quests=db_manager.get_user_quest_ids(user_id=message.from_user.id)),
    )
