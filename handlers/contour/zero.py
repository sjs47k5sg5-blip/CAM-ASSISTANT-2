from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .states import ContourWizard
from .ui import show_main_menu

router = Router()


# ==========================================
# НОЛЬ ДЕТАЛИ
# ==========================================

@router.callback_query(F.data == "zero")
async def zero_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎯 Центр",
                    callback_data="zero_CENTER"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↖ Левый верхний",
                    callback_data="zero_TL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↗ Правый верхний",
                    callback_data="zero_TR"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↙ Левый нижний",
                    callback_data="zero_BL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↘ Правый нижний",
                    callback_data="zero_BR"
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

    try:

        await callback.message.edit_text(

            "📍 <b>Ноль детали</b>\n\n"
            "Выберите положение нуля.",

            parse_mode="HTML",

            reply_markup=keyboard

        )

    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# СОХРАНИТЬ НОЛЬ ДЕТАЛИ
# ==========================================

@router.callback_query(
    F.data.in_(
        [
            "zero_CENTER",
            "zero_TL",
            "zero_TR",
            "zero_BL",
            "zero_BR",
        ]
    )
)
async def zero_save(
    callback: CallbackQuery,
    state: FSMContext
):

    zero = callback.data.replace("zero_", "")

    await state.update_data(
        zero=zero
    )

    await state.set_state(
        ContourWizard.menu
    )

    await show_main_menu(callback, state)


# ==========================================
# НОЛЬ ПО Z
# ==========================================

@router.callback_query(F.data == "zero_z")
async def zero_z_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="⬆ Верх детали",
                    callback_data="zeroz_TOP"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬇ Низ детали",
                    callback_data="zeroz_BOTTOM"
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

    try:

        await callback.message.edit_text(

            "📍 <b>Ноль по Z</b>\n\n"
            "Выберите положение нуля по оси Z.",

            parse_mode="HTML",

            reply_markup=keyboard

        )

    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# СОХРАНИТЬ НОЛЬ Z
# ==========================================

@router.callback_query(
    F.data.in_(
        [
            "zeroz_TOP",
            "zeroz_BOTTOM",
        ]
    )
)
async def zero_z_save(
    callback: CallbackQuery,
    state: FSMContext
):

    zero_z = callback.data.replace("zeroz_", "")

    await state.update_data(
        zero_z=zero_z
    )

    await state.set_state(
        ContourWizard.menu
    )

    await show_main_menu(callback, state)