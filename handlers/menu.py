from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from handlers.common import temp_text
from keyboards.inline_buttons import inline_buttons, Answer
from utils.create_answer import create_answer

router = Router()


def menu_buttons() -> InlineKeyboardMarkup:
    return inline_buttons(
        [Answer(id="create_quest", text="Создать новый квест"),
         Answer(id="my_quests_list", text="Посмотреть свои квесты"),
         Answer(id="quests_list", text="Перейти в каталог квестов")]
    )


def back_to_menu_button(onlyAnswer: bool = False) -> InlineKeyboardMarkup:
    answer = Answer(id="menu", text="Назад в меню")
    if onlyAnswer:
        return answer
    return inline_buttons([answer])


async def menu(input, state: FSMContext):
    await state.clear()
    await create_answer(input,
                        text=temp_text['menu'],
                        reply_markup=menu_buttons())


@router.message(Command(commands=["menu"]))
async def menu_message(message: Message, state: FSMContext):
    await menu(message, state)


@router.callback_query(text="menu")
async def menu_callback(callback: CallbackQuery, state: FSMContext):
    await menu(callback, state)
