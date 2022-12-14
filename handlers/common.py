import json

from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from utils.create_answer import message_answer

router = Router()

with open("message_templates.json", "r") as f:
    temp_text = json.load(f)


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message_answer(message, text=temp_text['start'])


@router.message()
async def error(message: Message, state: FSMContext):
    await state.clear()
    await message_answer(message, text=temp_text['error'])
