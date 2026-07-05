
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "CAM")
async def menu(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📐 Контур", callback_data="cam_contour")],
        [InlineKeyboardButton(text="⬜ Карман", callback_data="cam_pocket")]
    ])

    await message.answer("CAM MENU", reply_markup=kb)
