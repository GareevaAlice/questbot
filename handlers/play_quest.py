from aiogram import Router
from aiogram import html
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.common import temp_text
from handlers.menu import back_to_menu_button
from keyboards.reply_buttons import reply_buttons
from utils.DBManager import db_manager
from utils.Quest import Step
from utils.UserState import UserState
from utils.create_answer import message_answer

router = Router()


async def get_answers(step: Step, state: FSMContext, user_id: str,
                      quest_id: str) -> ReplyKeyboardMarkup:
    answers = [html.quote(answer.text) for answer in step.answers]
    if len(answers) == 0:
        await state.clear()
        db_manager.delete_user_state(user_id, quest_id)
        return ReplyKeyboardRemove()
    answers.append("Завершить квест")
    return reply_buttons(answers)


async def step_answer(message: Message, state: FSMContext, user_id: str, quest_id: str, step: Step):
    db_manager.save_step(user_id, quest_id, step)
    await message_answer(message,
                         text=html.quote(step.text),
                         reply_markup=await get_answers(step, state, user_id, quest_id))


def get_start_step(_: str, quest_id: str) -> Step:
    quest = db_manager.get_quest(quest_id)
    return quest.start_step


def get_current_step(user_id: str, quest_id: str) -> Step:
    return db_manager.get_current_step(user_id, quest_id)


async def first_step(callback: CallbackQuery, state: FSMContext, quest_id: str, get_step):
    await state.clear()
    await state.set_state(UserState.playing_quest)
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        step = get_step(callback.from_user.id, quest_id)
        await step_answer(callback.message, state, callback.from_user.id, quest_id, step)
        await state.update_data(quest_id=quest_id)
    except ValueError:
        await message_answer(callback.message,
                             text=temp_text['quest_id_error'],
                             reply_markup=back_to_menu_button())


@router.callback_query(Text(text_startswith="start_quest_"))
async def start_quest(callback: CallbackQuery, state: FSMContext):
    await first_step(callback, state, callback.data[len("start_quest_"):], get_start_step)


@router.callback_query(Text(text_startswith="continue_quest_"))
async def continue_quest(callback: CallbackQuery, state: FSMContext):
    await first_step(callback, state, callback.data[len("continue_quest_"):], get_current_step)


@router.message(Text(text=["Завершить квест"]), UserState.playing_quest)
async def stop_quest(message: Message, state: FSMContext):
    data = await state.get_data()
    quest_id = data.get('quest_id', '')
    await state.clear()
    await message_answer(message,
                         text=temp_text['stop_quest'].format(quest_id=quest_id))


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
                await step_answer(message, state, message.from_user.id, quest_id, step)
                await state.update_data(quest_id=quest_id)
                return
        await message_answer(message,
                             text=temp_text['play_error'],
                             reply_markup=await get_answers(current_step, state,
                                                            message.from_user.id, quest_id))
    except ValueError:
        await state.clear()
        await message_answer(message,
                             text=temp_text['step_error'])
