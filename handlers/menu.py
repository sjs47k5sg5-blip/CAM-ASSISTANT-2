from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from .cam_router import router as cam_router

router = Router()


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Фрезерование")],
        [KeyboardButton(text="🕳 Отверстия")],
        [KeyboardButton(text="📚 Справочник")]
    ],
    resize_keyboard=True
)


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("CAM Assistant", reply_markup=main_menu)


@router.message(F.text == "📐 Фрезерование")
async def milling(message: Message):
    await message.answer("Выберите операцию ниже ↓")