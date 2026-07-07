from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .states import ContourWizard

router = Router()


def status(value):
    return "✅" if value else "❌"


async def render_menu(state: FSMContext):

    data = await state.get_data()

    print("========== FSM ==========")
    print(data)
    print("=========================")

    text = (
        "📐 <b>КОНТУР</b>\n\n"
        f"{status(data.get('size_x') is not None)} Размер детали\n"
        f"{status(data.get('material') is not None)} Материал\n"
        f"{status(data.get('zero') is not None)} Ноль детали\n"
        f"{status(data.get('zero_z') is not None)} Ноль Z\n"
        f"{status(data.get('tool_diameter') is not None)} Инструмент\n"
        f"{status(data.get('corner_type') is not None)} Обработка углов\n"
        f"{status(data.get('allowance') is not None)} Припуск\n\n"
        "Выберите параметр:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📏 Размер детали",
                    callback_data="size"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧱 Материал",
                    callback_data="material"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📍 Ноль детали",
                    callback_data="zero"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📍 Ноль Z",
                    callback_data="zero_z"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙ Обработка углов",
                    callback_data="corner"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📉 Припуск",
                    callback_data="allowance"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔧 Инструмент",
                    callback_data="tool"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data="ready"
                )
            ]
        ]
    )

    return text, keyboard


@router.callback_query(F.data == "back_menu")
async def back_menu(callback: CallbackQuery, state: FSMContext):

    await state.set_state(ContourWizard.menu)

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