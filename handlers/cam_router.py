
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "cam_contour")
async def contour(c: CallbackQuery):
    await c.answer()
    await c.message.answer("Contour selected")

@router.callback_query(F.data == "cam_pocket")
async def pocket(c: CallbackQuery):
    await c.answer()
    await c.message.answer("Pocket selected")
