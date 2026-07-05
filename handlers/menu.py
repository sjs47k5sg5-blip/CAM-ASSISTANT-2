from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 CAM")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "/start")
async def start(m: Message):
    await m.answer("CAM CORE FULL READY", reply_markup=kb)
