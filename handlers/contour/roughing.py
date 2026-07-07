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
# ЧЕРНОВАЯ ОБРАБОТКА
# ==========================================

@router.callback_query(F.data == "roughing")
async def roughing_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="rough_yes"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="rough_no"
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
        "Выполнять черновую обработку?",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# БЕЗ ЧЕРНОВОЙ
# ==========================================

@router.callback_query(F.data == "rough_no")
async def rough_no(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(

        roughing_enabled=False

    )

    await show_main_menu(callback, state)


# ==========================================
# С ЧЕРНОВОЙ
# ==========================================

@router.callback_query(F.data == "rough_yes")
async def rough_yes(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(

        roughing_enabled=True

    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="40 %",
                    callback_data="stepover_0.4"
                )
            ],

            [
                InlineKeyboardButton(
                    text="50 %",
                    callback_data="stepover_0.5"
                )
            ],

            [
                InlineKeyboardButton(
                    text="60 %",
                    callback_data="stepover_0.6"
                )
            ],

            [
                InlineKeyboardButton(
                    text="70 %",
                    callback_data="stepover_0.7"
                )
            ],

            [
                InlineKeyboardButton(
                    text="80 %",
                    callback_data="stepover_0.8"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "📏 <b>Шаг по X/Y</b>\n\n"
        "Выберите боковой шаг.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ ШАГ
# ==========================================

@router.callback_query(F.data.startswith("stepover_"))
async def stepover_save(
    callback: CallbackQuery,
    state: FSMContext
):

    value = float(
        callback.data.replace(
            "stepover_",
            ""
        )
    )

    await state.update_data(

        roughing_stepover=value

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
            ]

        ]

    )

    await callback.message.edit_text(

        "🧭 <b>Направление обработки</b>",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# НАПРАВЛЕНИЕ
# ==========================================

@router.callback_query(F.data.startswith("dir_"))
async def direction_save(
    callback: CallbackQuery,
    state: FSMContext
):

    direction = callback.data.replace(
        "dir_",
        ""
    )

    await state.update_data(

        roughing_direction=direction

    )

    await show_main_menu(
        callback,
        state
    )