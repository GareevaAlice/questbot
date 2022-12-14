from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


async def message_answer(message: Message,
                         text: str,
                         reply_markup: str = ReplyKeyboardRemove()):
    await message.answer(
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


async def callback_answer(callback: CallbackQuery,
                          text: str,
                          reply_markup: str = ReplyKeyboardRemove()):
    await callback.message.edit_text(
        text=text,
        parse_mode="HTML"
    )
    await callback.message.edit_reply_markup(
        reply_markup=reply_markup
    )


async def create_answer(input,
                        text: str,
                        reply_markup: str = ReplyKeyboardRemove()):
    func = message_answer if type(input) == Message else callback_answer
    await func(input, text, reply_markup)
