import json
import xmltodict
import logging
import traceback

from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.inline_buttons import inline_buttons
from utils.DBManager import db_manager
from utils.QuestRunner import QuestRunner, QuestInfo, Step, Answer
from utils.UserState import UserState

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


@router.message(Command(commands=["quest_info"]))
async def ask_quest_id(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=temp_text['ask_quest_id'],
    )
    await state.set_state(UserState.getting_quest_info)


@router.message(UserState.getting_quest_info)
async def quest_info(message: Message, state: FSMContext):
    try:
        xml = db_manager.get_quest_xml(message.text)
        quest = xmltodict.parse(xml)
        quest_runner = QuestRunner(quest)
    except ValueError:
        await state.clear()
        await message.answer(
            text=temp_text['wrong_quest_id'],
        )
    else:
        info: QuestInfo = quest_runner.get_info()
        await message.answer(
            text=temp_text['quest_info'].format(id=message.text,
                                                name=info.name,
                                                summary=info.summary),
            reply_markup=inline_buttons([Answer(id="start",
                                                text=temp_text['quest_start'])])
        )
        await state.set_state(UserState.playing_quest)
        await state.update_data(quest_id=message.text)


@router.callback_query(UserState.playing_quest)
async def playing_quest(callback: CallbackQuery, state: FSMContext):
    try:
        quest_data = await state.get_data()
        quest_id = quest_data['quest_id']
        xml = db_manager.get_quest_xml(quest_id)

        quest = xmltodict.parse(xml)
        quest_runner = QuestRunner(quest)
        step: Step = quest_runner.get_step(prev_answer_id=callback.data)
    except ValueError:
        traceback.print_exc()
        await state.clear()
        await callback.message.answer(
            text=temp_text['error'],
        )
    else:
        await callback.message.answer(
            text=step.text,
            reply_markup=inline_buttons(step.answers)
        )
        await callback.message.edit_reply_markup(reply_markup=None)


@router.message(Command(commands=["quest_stop"]), UserState.playing_quest)
async def quest_end(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=temp_text['quest_stop'],
        reply_markup=ReplyKeyboardRemove()
    )
