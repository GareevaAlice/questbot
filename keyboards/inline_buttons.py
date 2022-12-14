from dataclasses import dataclass
from typing import List

from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass
class Answer:
    id: str
    text: str


def inline_buttons(answers: List[Answer]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=answer.text,
                                     callback_data=answer.id)] for answer in answers]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
