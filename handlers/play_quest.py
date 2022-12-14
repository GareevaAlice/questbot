import json

from aiogram import Router
from aiogram import html
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.menu import back_to_menu_button
from keyboards.inline_buttons import Answer, inline_buttons
from keyboards.reply_buttons import reply_buttons
from utils.DBManager import db_manager
from utils.Quest import Step
from utils.UserState import UserState
from utils.create_answer import message_answer

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


async def step_answer(message: Message, user_id: str, quest_id: str, step: Step):
    db_manager.save_step(user_id, quest_id, step)
    answers = [html.quote(answer.text) for answer in step.answers]
    answers.append("Завершить квест")
    await message_answer(message,
                         text=html.quote(step.text),
                         reply_markup=reply_buttons(answers))


@router.callback_query(Text(text_startswith="start_quest_"))
async def start_quest_(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserState.playing_quest)
    await callback.message.edit_reply_markup(reply_markup=None)
    quest_id = callback.data[len("start_quest_"):]
    try:
        quest = db_manager.get_quest(quest_id)
        await step_answer(callback.message, callback.from_user.id, quest_id, quest.begin_step)
        await state.update_data(quest_id=quest_id)
    except ValueError:
        await message_answer(callback.message,
                             text=temp_text['wrong_quest_id'],
                             reply_markup=back_to_menu_button())


@router.message(Text(text=["Завершить квест"]), UserState.playing_quest)
async def stop_quest(message: Message, state: FSMContext):
    data = await state.get_data()
    quest_id = data.get('quest_id', '')
    await state.clear()
    await message_answer(
        message,
        text=temp_text['stop_quest'].format(quest_id=quest_id),
        reply_markup=inline_buttons([Answer(id=f"quest_{quest_id}", text="О квесте"),
                                     back_to_menu_button(onlyAnswer=True)]))


@router.message(UserState.playing_quest)
async def play_quest(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        quest_id = data.get('quest_id', '')
        current_step = db_manager.get_current_step(message.from_user.id, quest_id)
        for answer in current_step.answers:
            if answer.text == message.text:
                quest = db_manager.get_quest(quest_id)
                step = quest.get_step(answer.next_step_id)
                await step_answer(message, message.from_user.id, quest_id, step)
                await state.update_data(quest_id=quest_id)
                return
        await message_answer(message,
                             text=temp_text['play_error'])
    except ValueError:
        await state.clear()
        await message_answer(message,
                             text=temp_text['error'],
                             reply_markup=back_to_menu_button())
