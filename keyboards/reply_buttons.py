from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def reply_buttons(answers: List[str]) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=answer)] for answer in answers]
    return ReplyKeyboardMarkup(keyboard=buttons,
                               resize_keyboard=True)
