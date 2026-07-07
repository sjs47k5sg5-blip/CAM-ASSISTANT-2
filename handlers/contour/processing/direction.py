from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from ..states import ContourWizard

router = Router()


# ==========================================
# НАПРАВЛЕНИЕ ОБРАБОТКИ
# ==========================================

@router.callback_query(F.data.in_(["dir_CLIMB", "dir_CONVENTIONAL"]))
async def direction_save(
    callback: CallbackQuery,
    state: FSMContext,
):

    direction = callback.data.replace("dir_", "")

    await state.update_data(
        cut_direction=direction
    )

    await state.set_state(
        ContourWizard.allowance
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="0",
                    callback_data="allowance_0"
                ),
                InlineKeyboardButton(
                    text="0.2",
                    callback_data="allowance_0.2"
                ),
            ],

            [
                InlineKeyboardButton(
                    text="0.5",
                    callback_data="allowance_0.5"
                ),
                InlineKeyboardButton(
                    text="1.0",
                    callback_data="allowance_1.0"
                ),
            ],

            [
                InlineKeyboardButton(
                    text="✏️ Ввести своё значение",
                    callback_data="allowance_custom"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="processing"
                )
            ]

        ]
    )

    await callback.message.edit_text(

        "📉 <b>Припуск</b>\n\n"
        "Выберите припуск или введите своё значение.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()