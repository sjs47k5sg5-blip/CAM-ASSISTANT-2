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
# ЗАПУСК МАСТЕРА
# ==========================================

@router.callback_query(F.data == "processing")
async def processing_start(
    callback: CallbackQuery,
    state: FSMContext,
):

    await state.set_state(
        ContourWizard.roughing
    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="roughing_yes"
                ),

                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="roughing_no"
                )

            ],

            [

                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )

            ]

        ]

    )

    await callback.message.edit_text(

        "🪓 <b>Черновая обработка</b>\n\n"
        "Использовать черновую обработку?",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ
# ==========================================

@router.callback_query(
    F.data.in_(
        [
            "roughing_yes",
            "roughing_no"
        ]
    )
)
async def roughing_save(
    callback: CallbackQuery,
    state: FSMContext,
):

    enabled = callback.data == "roughing_yes"

    await state.update_data(

        roughing_enabled=enabled

    )

    await state.set_state(

        ContourWizard.step_z

    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(
                    text="1 мм",
                    callback_data="stepz_1"
                ),

                InlineKeyboardButton(
                    text="2 мм",
                    callback_data="stepz_2"
                ),

                InlineKeyboardButton(
                    text="3 мм",
                    callback_data="stepz_3"
                )

            ]

        ]

    )

    await callback.message.edit_text(

        "📏 <b>Шаг по Z</b>\n\n"
        "Выберите шаг обработки.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()