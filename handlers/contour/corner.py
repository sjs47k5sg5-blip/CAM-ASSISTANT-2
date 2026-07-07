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
from .ui import show_main_menu

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
                    text="⬜ Острые углы",
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
            "Выберите тип обработки.",
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

        await state.set_state(ContourWizard.menu)

        await show_main_menu(callback, state)

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
        "Выберите углы для обработки.",
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
        "Введите радиус или фаску (мм).\n\n"
        "<code>2</code>",
        parse_mode="HTML"
    )

    await callback.answer()


# ==========================================
# ВВОД РАЗМЕРА
# ==========================================

@router.message(ContourWizard.corner_value)
async def corner_value(message: Message, state: FSMContext):

    try:

        value = float(message.text.replace(",", "."))

        if value < 0:
            raise ValueError

    except ValueError:

        await message.answer(
            "❌ Введите корректное число."
        )

        return

    await state.update_data(
        corner_value=value
    )

    await state.set_state(
        ContourWizard.menu
    )

    await message.answer(
        f"✅ Размер сохранён: {value} мм"
    )

    await show_main_menu(message, state)