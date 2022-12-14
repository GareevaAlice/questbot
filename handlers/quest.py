import json

from aiogram import Router
from aiogram import html
from aiogram.dispatcher.filters import Command, CommandObject, Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from handlers.menu import back_to_menu_button
from keyboards.inline_buttons import inline_buttons, Answer
from utils.DBManager import db_manager
from utils.Quest import QuestInfo
from utils.create_answer import create_answer

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


def quest_text(quest_info: QuestInfo) -> str:
    return temp_text['quest'].format(
        quest_id=html.quote(quest_info.id),
        title=html.quote(quest_info.title),
        summary=html.quote(quest_info.summary),
    )


def quest_buttons(quest_id: str, list_type: str) -> InlineKeyboardMarkup:
    return inline_buttons(
        [Answer(id=f"start_quest_{quest_id}", text="Пройти квест"),
         Answer(id=(list_type if list_type else "quests_list"), text="Вернуться к списку"), ]
    )


async def quest(input, state: FSMContext, quest_id: str):
    data = await state.get_data()
    list_type = data.get('list_type', '')
    await state.clear()
    try:
        quest_info = db_manager.get_quest(quest_id).quest_info
    except ValueError:
        await create_answer(input,
                            text=temp_text['wrong_quest_id'],
                            reply_markup=back_to_menu_button())
    else:
        await create_answer(input,
                            text=quest_text(quest_info),
                            reply_markup=quest_buttons(quest_id, list_type))


@router.message(Command(commands=["quest"]))
async def quest_message(message: Message, command: CommandObject, state: FSMContext):
    await quest(message, state, quest_id=command.args)


@router.callback_query(Text(text_startswith="quest_"))
async def quest_callback(callback: CallbackQuery, state: FSMContext):
    await quest(callback, state, quest_id=callback.data[len("quest_"):])
