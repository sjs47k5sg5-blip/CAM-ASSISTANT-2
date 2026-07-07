from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .menu import render_menu

router = Router()


# ==========================================
# ПРИПУСК
# ==========================================

@router.callback_query(F.data == "allowance")
async def allowance_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="0 мм",
                    callback_data="allow_0"
                )
            ],

            [
                InlineKeyboardButton(
                    text="0.2 мм",
                    callback_data="allow_0.2"
                )
            ],

            [
                InlineKeyboardButton(
                    text="0.5 мм",
                    callback_data="allow_0.5"
                )
            ],

            [
                InlineKeyboardButton(
                    text="1.0 мм",
                    callback_data="allow_1.0"
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
            "📉 <b>Припуск</b>\n\n"
            "Выберите величину припуска.",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# СОХРАНИТЬ ПРИПУСК
# ==========================================

@router.callback_query(F.data.startswith("allow_"))
async def allowance_save(
    callback: CallbackQuery,
    state: FSMContext
):

    allowance = float(callback.data.replace("allow_", ""))

    await state.update_data(
        allowance=allowance
    )

    if allowance == 0:

        await state.update_data(
            finish_pass=False,
            finish_tool=False
        )

        text, kb = await render_menu(state)

        try:
            await callback.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=kb
            )
        except TelegramBadRequest:
            pass

        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="finish_yes"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="finish_no"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "Выполнять чистовой проход?",
        reply_markup=keyboard
    )

    await callback.answer()


# ==========================================
# БЕЗ ЧИСТОВОГО
# ==========================================

@router.callback_query(F.data == "finish_no")
async def finish_no(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_pass=False,
        finish_tool=False
    )

    text, kb = await render_menu(state)

    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=kb
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# ЧИСТОВОЙ
# ==========================================

@router.callback_query(F.data == "finish_yes")
async def finish_yes(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_pass=True
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="Тем же инструментом",
                    callback_data="finish_same"
                )
            ],

            [
                InlineKeyboardButton(
                    text="Другим инструментом",
                    callback_data="finish_other"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "Выберите инструмент для чистового прохода.",
        reply_markup=keyboard
    )

    await callback.answer()


# ==========================================
# ТЕМ ЖЕ ИНСТРУМЕНТОМ
# ==========================================

@router.callback_query(F.data == "finish_same")
async def finish_same(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_tool=False
    )

    text, kb = await render_menu(state)

    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=kb
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# ДРУГИМ ИНСТРУМЕНТОМ
# ==========================================

@router.callback_query(F.data == "finish_other")
async def finish_other(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_tool=True
    )

    text, kb = await render_menu(state)

    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=kb
        )
    except TelegramBadRequest:
        pass

    await callback.answer()