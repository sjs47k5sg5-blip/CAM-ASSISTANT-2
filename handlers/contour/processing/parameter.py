from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

router = Router()


async def show_parameter(
    callback: CallbackQuery,
    state: FSMContext,
    *,
    title: str,
    parameter: str,
    values: list[tuple[str, float]],
    next_callback: str,
):

    keyboard = []

    row = []

    for text, value in values:

        row.append(

            InlineKeyboardButton(

                text=text,

                callback_data=f"{next_callback}:{value}"

            )

        )

        if len(row) == 2:

            keyboard.append(row)

            row = []

    if row:
        keyboard.append(row)

    keyboard.append(

        [

            InlineKeyboardButton(

                text="✏️ Ввести своё значение",

                callback_data=f"custom:{parameter}"

            )

        ]

    )

    keyboard.append(

        [

            InlineKeyboardButton(

                text="⬅ Назад",

                callback_data="processing"

            )

        ]

    )

    await callback.message.edit_text(

        f"<b>{title}</b>\n\n"
        "Выберите значение.",

        parse_mode="HTML",

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )

    )

    await callback.answer()