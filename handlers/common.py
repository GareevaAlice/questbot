import json

from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from utils.UserState import UserState

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=temp_text['start'],
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["help"]), UserState.playing_quest)
async def playing_quest_help(message: Message):
    await message.answer(
        text=f"{temp_text['playing_quest_help']}\n\n"
             f"{temp_text['playing_quest_commands']}",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["help"]))
async def common_help(message: Message):
    await message.answer(
        text=f"{temp_text['common_help']}\n\n"
             f"{temp_text['common_commands']}\n"
             f"{temp_text['playing_quest_commands']}\n"
             f"{temp_text['creating_quest_commands']}",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message()
async def error(message: Message):
    await message.answer(
        text=temp_text['error'],
        reply_markup=ReplyKeyboardRemove()
    )
