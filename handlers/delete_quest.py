from aiogram import Router
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.common import temp_text
from handlers.menu import back_to_menu_button
from keyboards.inline_buttons import inline_buttons, Answer
from utils.DBManager import db_manager
from utils.create_answer import callback_answer

router = Router()


@router.callback_query(Text(text_startswith="delete_quest_"))
async def delete_quest(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    quest_id = callback.data[len("delete_quest_"):]
    if db_manager.is_author(callback.from_user.id, quest_id):
        db_manager.delete_quest(callback.from_user.id, quest_id)
        await callback_answer(callback,
                              text=temp_text['delete_quest'],
                              reply_markup=inline_buttons(
                                  [Answer(id="my_quests_list", text="Вернуться к списку")]))
    else:
        await callback_answer(callback,
                              text=temp_text['delete_error'],
                              reply_markup=back_to_menu_button())
