import json

from aiogram import Router, Bot
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ContentType

from utils.DBManager import db_manager
from utils.UserState import UserState
from utils.XMLChecker import XMLChecker

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


@router.message(Command(commands=["quest_create"]))
async def ask_quest_xml(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=temp_text['ask_quest_xml'],
    )
    await state.set_state(UserState.getting_quest_xml)


@router.message(UserState.getting_quest_xml, content_types=ContentType.DOCUMENT)
async def quest_create(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    file_path = f"/tmp/{message.document.file_id}.xml"
    await bot.download(
        message.document,
        destination=file_path
    )
    xml_checker = XMLChecker(file_path)
    if xml_checker.is_correct():
        db_manager.save_quest()
        await message.answer(
            text=message.document.file_id,
        )
    else:
        await message.answer(
            text=temp_text['wrong_quest_xml'],
        )
