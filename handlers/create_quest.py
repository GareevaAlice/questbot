import json
import logging

from aiogram import Router, Bot
from aiogram import html
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery

from handlers.menu import back_to_menu_button
from handlers.quest import quest_text, quest_buttons
from keyboards.inline_buttons import inline_buttons, Answer
from utils.DBManager import db_manager, tmp_folder
from utils.UserState import UserState
from utils.create_answer import message_answer, create_answer

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


async def ask_quest_xml(input, state: FSMContext):
    await state.clear()
    await create_answer(input,
                        text=temp_text['ask_quest_xml'],
                        reply_markup=back_to_menu_button())
    await state.set_state(UserState.getting_quest_xml)


@router.message(Command(commands=["create_quest"]))
async def ask_quest_xml_message(message: Message, state: FSMContext):
    await ask_quest_xml(message, state)


@router.callback_query(text="create_quest")
async def ask_quest_xml_callback(callback: CallbackQuery, state: FSMContext):
    await ask_quest_xml(callback, state)


@router.message(UserState.getting_quest_xml, content_types=ContentType.DOCUMENT)
async def create_quest(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    quest_id = message.document.file_unique_id
    file_path = f"{tmp_folder}/{quest_id}.xml"
    await bot.download(
        message.document,
        destination=file_path
    )
    try:
        quest_info = db_manager.save_quest(file_path, message.from_user.id).quest_info
    except Exception as e:
        logging.warning(e)
        await message_answer(
            message,
            text=temp_text['wrong_quest_xml'].format(error=html.quote(str(e))),
            reply_markup=inline_buttons(
                [Answer(id="create_quest", text="Попробовать ещё раз")]
            )
        )
    else:
        await message_answer(message,
                             text=quest_text(quest_info),
                             reply_markup=quest_buttons(message.from_user.id,
                                                        quest_id,
                                                        "my_quests_list"))
