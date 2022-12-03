import json
import logging

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
    schema_path = f'/app/default_schema.xsd'
    xml_checker = XMLChecker(schema_path)
    try:
        xml_checker.check(file_path)
    except Exception as e:
        logging.warning(e)
        await message.answer(
            text=temp_text['wrong_quest_xml'].format(error=str(e)),
            parse_mode="MarkdownV2"
        )
    else:
        db_manager.save_quest(message.from_user.id, message.document.file_id)
        await message.answer(
            text=temp_text['quest_create'].format(quest_id=message.document.file_id),
            parse_mode="MarkdownV2"
        )
