from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "⬅️ Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu
    )