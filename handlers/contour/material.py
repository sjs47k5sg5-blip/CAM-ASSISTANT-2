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


@router.callback_query(F.data == "material")
async def material_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟦 Алюминий",
                    callback_data="mat_ALUMINUM"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬛ Сталь",
                    callback_data="mat_STEEL"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟨 Латунь",
                    callback_data="mat_BRASS"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟧 Медь",
                    callback_data="mat_COPPER"
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
            "🧱 <b>Материал</b>\n\n"
            "Выберите материал.",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


@router.callback_query(F.data.startswith("mat_"))
async def material_save(
    callback: CallbackQuery,
    state: FSMContext
):

    material = callback.data.replace("mat_", "")

    await state.update_data(
        material=material
    )

    await state.set_state(
        ContourWizard.menu
    )

    await show_main_menu(callback, state)