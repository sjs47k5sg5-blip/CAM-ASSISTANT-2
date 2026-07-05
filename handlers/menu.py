from aiogram import Router, F
from aiogram.types import Message

router = Router()


# =========================
# MAIN MENU HANDLER
# =========================
@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "CAM PRO READY\n\n"
        "Выберите функцию из меню ниже."
    )


# =========================
# CAM BUTTON ENTRY
# =========================
@router.message(F.text == "📐 Контур")
async def open_cam(message: Message):
    await message.answer(
        "Перейдите в CAM раздел (кнопка 📐 Контур)."
    )