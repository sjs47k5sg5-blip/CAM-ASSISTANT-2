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
# ШАГ ПО Z
# ==========================================

@router.callback_query(F.data.startswith("stepz_"))
async def step_z_save(
    callback: CallbackQuery,
    state: FSMContext,
):

    step = float(
        callback.data.replace(
            "stepz_",
            ""
        )
    )

    await state.update_data(
        step_z=step
    )

    await state.set_state(
        ContourWizard.stepover
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="20%",
                    callback_data="stepover_0.2"
                ),
                InlineKeyboardButton(
                    text="40%",
                    callback_data="stepover_0.4"
                ),
            ],

            [
                InlineKeyboardButton(
                    text="60%",
                    callback_data="stepover_0.6"
                ),
                InlineKeyboardButton(
                    text="80%",
                    callback_data="stepover_0.8"
                ),
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

        "📐 <b>Боковой шаг (Stepover)</b>\n\n"
        "Выберите процент от диаметра инструмента.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()