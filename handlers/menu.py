from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from services.ui_state import ui_state

router = Router()


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Фрезерование")],
        [KeyboardButton(text="🕳 Отверстия")],
        [KeyboardButton(text="📚 Справочник")],
        [KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)


@router.message(F.text == "/start")
async def start(message: Message):

    ui_state.reset()

    await message.answer(
        "👋 CAM Assistant Pro",
        reply_markup=main_menu
    )