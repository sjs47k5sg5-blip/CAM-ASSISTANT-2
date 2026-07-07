from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .states import ContourWizard
from .menu import render_menu

router = Router()


# ==========================================
# ОБРАБОТКА УГЛОВ
# ==========================================

@router.callback_query(F.data == "corner")
async def corner_click(callback: CallbackQuery, state: FSMContext):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔵 Радиус",
                    callback_data="corner_RADIUS"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔶 Фаска",
                    callback_data="corner_CHAMFER"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬜ Острые",
                    callback_data="corner_SHARP"
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
            "⚙ <b>Обработка углов</b>\n\n"
            "Выберите тип.",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


# ==========================================
# ТИП УГЛОВ
# ==========================================

@router.callback_query(F.data.startswith("corner_"))
async def corner_type(callback: CallbackQuery, state: FSMContext):

    corner = callback.data.replace("corner_", "")

    if corner == "SHARP":

        await state.update_data(
            corner_type="SHARP",
            corner_select="ALL",
            corner_value=0
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

    await state.update_data(
        corner_type=corner
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Все углы",
                    callback_data="cornerpos_ALL"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↖ Левый верхний",
                    callback_data="cornerpos_TL"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↗ Правый верхний",
                    callback_data="cornerpos_TR"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↙ Левый нижний",
                    callback_data="cornerpos_BL"
                )
            ],
            [
                InlineKeyboardButton(
                    text="↘ Правый нижний",
                    callback_data="cornerpos_BR"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="corner"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "Выберите углы.",
        reply_markup=keyboard
    )

    await callback.answer()


# ==========================================
# ВЫБОР УГЛОВ
# ==========================================

@router.callback_query(F.data.startswith("cornerpos_"))
async def corner_position(callback: CallbackQuery, state: FSMContext):

    position = callback.data.replace("cornerpos_", "")

    await state.update_data(
        corner_select=position
    )

    await state.set_state(
        ContourWizard.corner_value
    )

    await callback.message.answer(
        "Введите размер радиуса или фаски.\n\n"
        "Например:\n"
        "<code>2</code>",
        parse_mode="HTML"
    )

    await callback.answer()


# ==========================================
# РАЗМЕР
# ==========================================

@router.message(ContourWizard.corner_value)
async def corner_value(
    message: Message,
    state: FSMContext
):

    try:

        value = float(
            message.text.replace(",", ".")
        )

        if value < 0:
            raise ValueError

    except ValueError:

        await message.answer(
            "Введите корректное число."
        )

        return

    await state.update_data(
        corner_value=value
    )

    await state.set_state(
        ContourWizard.menu
    )

    text, kb = await render_menu(state)

    await message.answer(
        f"✅ Размер {value} мм сохранён."
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=kb
    )