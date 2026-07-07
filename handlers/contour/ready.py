from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

router = Router()


# ==========================================
# ГОТОВО
# ==========================================

@router.callback_query(F.data == "ready")
async def ready_click(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    errors = []

    if data.get("size_x") is None:
        errors.append("• Размер детали")

    if data.get("material") is None:
        errors.append("• Материал")

    if data.get("zero") is None:
        errors.append("• Ноль детали")

    if data.get("zero_z") is None:
        errors.append("• Ноль по Z")

    if data.get("tool_diameter") is None:
        errors.append("• Инструмент")

    if errors:

        await callback.message.answer(

            "❌ Заполнены не все параметры.\n\n"
            "Необходимо заполнить:\n\n"
            + "\n".join(errors)

        )

        await callback.answer()

        return

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="▶ Сгенерировать G-код",
                    callback_data="generate"
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

        "✅ Все параметры заполнены.\n\n"
        "Можно приступать к генерации программы.",

        reply_markup=keyboard

    )

    await callback.answer()