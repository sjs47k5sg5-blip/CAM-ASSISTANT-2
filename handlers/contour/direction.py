from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from .ui import show_main_menu

router = Router()


# ==========================================
# НАПРАВЛЕНИЕ ОБРАБОТКИ
# ==========================================

@router.callback_query(F.data == "direction")
async def direction_click(
    callback: CallbackQuery,
    state: FSMContext
):

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
                    callback_data="back_menu"
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


# ==========================================
# СОХРАНИТЬ НАПРАВЛЕНИЕ
# ==========================================

@router.callback_query(
    F.data.in_(
        [
            "dir_CLIMB",
            "dir_CONVENTIONAL",
        ]
    )
)
async def direction_save(
    callback: CallbackQuery,
    state: FSMContext
):

    direction = callback.data.replace(
        "dir_",
        ""
    )

    await state.update_data(

        cut_direction=direction

    )

    await show_main_menu(
        callback,
        state
    )