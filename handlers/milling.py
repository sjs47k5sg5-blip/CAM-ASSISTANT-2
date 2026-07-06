from aiogram import Router, F
from aiogram.types import Message

from services.cam_engine import contour

router = Router()


@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):
    await message.answer(
        "⚙ ФРЕЗЕРОВКА\n\n"
        "📐 Контур (активен)\n"
        "📦 Карман (будет)\n"
        "📏 Обводка (будет)"
    )


@router.message(F.text == "📐 Контур")
async def contour_entry(message: Message):
    await message.answer(
        "📐 КОНТУР CAM\n\n"
        "Введите X Y Z"
    )