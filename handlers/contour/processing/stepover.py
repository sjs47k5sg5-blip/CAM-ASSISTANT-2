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
# БОКОВОЙ ШАГ
# ==========================================

@router.callback_query(F.data.startswith("stepover_"))
async def stepover_save(
    callback: CallbackQuery,
    state: FSMContext,
):

    stepover = float(
        callback.data.replace(
            "stepover_",
            ""
        )
    )

    await state.update_data(
        roughing_stepover=stepover
    )

    await state.set_state(
        ContourWizard.direction
    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(
                    text="➡ Попутное",
                    callback_data="dir_CLIMB"
                )

            ],

            [

                InlineKeyboardButton(
                    text="⬅ Встречное",
                    callback_data="dir_CONVENTIONAL"
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

        "🧭 <b>Направление обработки</b>\n\n"
        "Выберите направление фрезерования.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()