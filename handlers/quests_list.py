import json
import logging
from typing import List

from aiogram import Router
from aiogram import html
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from handlers.menu import back_to_menu_button
from keyboards.inline_buttons import inline_buttons, Answer
from utils.DBManager import db_manager
from utils.create_answer import create_answer

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


def my_quests_list_text() -> str:
    return temp_text['my_quests_list']


def quests_list_text() -> str:
    return temp_text['quests_list']


def quests_list_buttons(quest_ids: List[str]) -> InlineKeyboardMarkup:
    answers = []
    for quest_id in quest_ids:
        quest_info = db_manager.get_quest(quest_id).quest_info
        answers.append(Answer(id=f"quest_{quest_id}",
                              text=html.quote(quest_info.title)))
    answers.append(back_to_menu_button(onlyAnswer=True))
    return inline_buttons(answers)


async def my_quests_list(input, state: FSMContext, user_id: str):
    await state.clear()
    quest_ids = db_manager.get_user_quest_ids(user_id)
    await create_answer(input,
                        text=my_quests_list_text(),
                        reply_markup=quests_list_buttons(quest_ids))
    await state.update_data(list_type="my_quests_list")


async def quests_list(input, state: FSMContext):
    await state.clear()
    quest_ids = db_manager.get_catalog_quest_ids()
    await create_answer(input,
                        text=quests_list_text(),
                        reply_markup=quests_list_buttons(quest_ids))
    await state.update_data(list_type="quests_list")


@router.message(Command(commands=["my_quests_list"]))
async def my_quests_list_message(message: Message, state: FSMContext):
    logging.info(message.from_user.id)
    await my_quests_list(message, state, user_id=message.from_user.id)


@router.callback_query(text="my_quests_list")
async def my_quests_list_callback(callback: CallbackQuery, state: FSMContext):
    await my_quests_list(callback, state, user_id=callback.from_user.id)


@router.message(Command(commands=["quests_list"]))
async def quests_list_message(message: Message, state: FSMContext):
    await quests_list(message, state)


@router.callback_query(text="quests_list")
async def quests_list_callback(callback: CallbackQuery, state: FSMContext):
    await quests_list(callback, state)
