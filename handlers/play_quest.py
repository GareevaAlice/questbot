from typing import List

from aiogram import Router
from aiogram import html
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.common import temp_text
from handlers.menu import back_to_menu_button
from keyboards.reply_buttons import reply_buttons
from utils.DBManager import db_manager, PlayState
from utils.Quest import Answer
from utils.UserState import UserState
from utils.create_answer import message_answer

router = Router()


def get_answers(play_state: PlayState) -> List[Answer]:
    answers = []
    for answer in play_state.current_step.answers:
        append = True
        if len(answer.visited):
            for visited in answer.visited:
                append &= (visited in play_state.visited)
        if len(answer.not_visited):
            for not_visited in answer.not_visited:
                append &= (not_visited not in play_state.visited)
        if append:
            answers.append(answer)
    return answers


async def get_answers_buttons(play_state: PlayState, state: FSMContext, user_id: str,
                              quest_id: str) -> ReplyKeyboardMarkup:
    answers = [html.quote(answer.text) for answer in get_answers(play_state)]
    if len(answers) == 0:
        await state.clear()
        db_manager.delete_play_state(user_id, quest_id)
        return ReplyKeyboardRemove()
    answers.append("Завершить квест")
    return reply_buttons(answers)


async def step_answer(message: Message, state: FSMContext, user_id: str, quest_id: str,
                      play_state: PlayState):
    play_state.visited.add(play_state.current_step.id)
    db_manager.save_play_state(user_id, quest_id, play_state)
    await message_answer(message,
                         text=html.quote(play_state.current_step.text),
                         reply_markup=await get_answers_buttons(play_state, state, user_id,
                                                                quest_id))


def get_start_play_state(_: str, quest_id: str) -> PlayState:
    quest = db_manager.get_quest(quest_id)
    return PlayState(current_step=quest.start_step,
                     visited=set())


def get_current_play_state(user_id: str, quest_id: str) -> PlayState:
    return db_manager.get_current_play_state(user_id, quest_id)


async def first_step(callback: CallbackQuery, state: FSMContext, quest_id: str, get_play_state):
    await state.clear()
    await state.set_state(UserState.playing_quest)
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        play_state = get_play_state(callback.from_user.id, quest_id)
        await step_answer(callback.message, state, callback.from_user.id, quest_id, play_state)
        await state.update_data(quest_id=quest_id)
    except ValueError:
        await message_answer(callback.message,
                             text=temp_text['quest_id_error'],
                             reply_markup=back_to_menu_button())


@router.callback_query(Text(text_startswith="start_quest_"))
async def start_quest(callback: CallbackQuery, state: FSMContext):
    await first_step(callback, state, callback.data[len("start_quest_"):], get_start_play_state)


@router.callback_query(Text(text_startswith="continue_quest_"))
async def continue_quest(callback: CallbackQuery, state: FSMContext):
    await first_step(callback, state, callback.data[len("continue_quest_"):],
                     get_current_play_state)


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
        play_state = db_manager.get_current_play_state(message.from_user.id, quest_id)
        for answer in get_answers(play_state):
            if answer.text == message.text:
                quest = db_manager.get_quest(quest_id)
                step = quest.get_step(answer.next_step_id)
                await step_answer(message, state, message.from_user.id, quest_id,
                                  PlayState(current_step=step, visited=play_state.visited))
                await state.update_data(quest_id=quest_id)
                return
        await message_answer(message,
                             text=temp_text['play_error'],
                             reply_markup=await get_answers_buttons(play_state, state,
                                                                    message.from_user.id, quest_id))
    except ValueError:
        await state.clear()
        await message_answer(message,
                             text=temp_text['step_error'])
