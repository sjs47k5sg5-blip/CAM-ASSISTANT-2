from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.fsm.context import FSMContext

from .states import ContourWizard
from .ui import show_main_menu

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
        "Введите номер инструмента и диаметр.\n\n"
        "<code>3 10</code>\n\n"
        "где\n"
        "3 -- номер инструмента\n"
        "10 -- диаметр фрезы",

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

    except ValueError:

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
        ContourWizard.step_z
    )

    await message.answer(

        f"✅ Инструмент сохранён\n\n"
        f"T{tool}\n"
        f"Ø{diameter} мм"

    )

    await message.answer(

        "📏 <b>Шаг по глубине</b>\n\n"
        "Введите шаг по Z (мм).\n\n"
        "Например:\n"
        "<code>2</code>",

        parse_mode="HTML"

    )


# ==========================================
# ШАГ ПО ГЛУБИНЕ
# ==========================================

@router.message(ContourWizard.step_z)
async def step_z_input(
    message: Message,
    state: FSMContext
):

    try:

        step = float(
            message.text.replace(",", ".")
        )

        if step <= 0:
            raise ValueError

    except ValueError:

        await message.answer(

            "❌ Неверное значение.\n\n"
            "Введите положительное число.\n\n"
            "Например:\n"
            "<code>2</code>",

            parse_mode="HTML"

        )

        return

    await state.update_data(
        step_z=step
    )

    await state.set_state(
        ContourWizard.menu
    )

    await message.answer(

        f"✅ Шаг по глубине сохранён\n\n"
        f"{step} мм"

    )

    await show_main_menu(
        message,
        state
    )