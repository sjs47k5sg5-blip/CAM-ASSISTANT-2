from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .states import ContourWizard
from .ui import show_main_menu

router = Router()


# ==========================================
# РАЗМЕР ДЕТАЛИ
# ==========================================

@router.callback_query(F.data == "size")
async def size_click(callback: CallbackQuery, state: FSMContext):

    await state.set_state(ContourWizard.size)

    await callback.message.answer(
        "📏 <b>Размер детали</b>\n\n"
        "Введите размеры детали.\n\n"
        "Формат:\n"
        "<code>30 20 15</code>\n\n"
        "X Y Z",
        parse_mode="HTML"
    )

    await callback.answer()


# ==========================================
# ВВОД РАЗМЕРОВ
# ==========================================

@router.message(ContourWizard.size)
async def size_input(message: Message, state: FSMContext):

    try:

        values = message.text.replace(",", ".").split()

        if len(values) != 3:
            raise ValueError

        x = float(values[0])
        y = float(values[1])
        z = float(values[2])

        if x <= 0 or y <= 0 or z <= 0:
            raise ValueError

    except ValueError:

        await message.answer(
            "❌ Неверный формат.\n\n"
            "Введите:\n"
            "<code>30 20 15</code>",
            parse_mode="HTML"
        )

        return

    await state.update_data(
        size_x=x,
        size_y=y,
        size_z=z
    )

    await state.set_state(ContourWizard.menu)

    # Только одно информационное сообщение
    await message.answer(
        f"✅ Размер сохранён\n\n"
        f"X = {x}\n"
        f"Y = {y}\n"
        f"Z = {z}"
    )

    # Возвращаемся в единое меню
    await show_main_menu(message, state)