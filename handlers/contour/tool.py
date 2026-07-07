from aiogram import Router
from aiogram import F
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.fsm.context import FSMContext

from .states import ContourWizard
from .menu import render_menu

router = Router()


# ==========================================
# ИНСТРУМЕНТ
# ==========================================

@router.callback_query(F.data == "tool")
async def tool_click(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(ContourWizard.tool)

    await callback.message.answer(

        "🔧 <b>Инструмент</b>\n\n"

        "Введите:\n\n"

        "<code>Номер Диаметр</code>\n\n"

        "Например:\n"

        "<code>3 10</code>",

        parse_mode="HTML"

    )

    await callback.answer()


# ==========================================
# ВВОД ИНСТРУМЕНТА
# ==========================================

@router.message(ContourWizard.tool)
async def tool_input(
    message: Message,
    state: FSMContext
):

    try:

        values = message.text.replace(",", ".").split()

        if len(values) != 2:
            raise ValueError

        tool = int(values[0])
        diameter = float(values[1])

        if tool <= 0:
            raise ValueError

        if diameter <= 0:
            raise ValueError

    except Exception:

        await message.answer(

            "❌ Неверный формат.\n\n"

            "Введите:\n"

            "<code>3 10</code>",

            parse_mode="HTML"

        )

        return

    await state.update_data(

        tool_number=tool,

        tool_diameter=diameter

    )

    await state.set_state(
        ContourWizard.menu
    )

    text, kb = await render_menu(state)

    await message.answer(

        "✅ Инструмент сохранён\n\n"

        f"T{tool}\n"

        f"Ø{diameter} мм"

    )

    await message.answer(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )