from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu
from database import register_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )

    await message.answer(
        "👋 Добро пожаловать в CNC Assistant Pro!",
        reply_markup=main_menu,
    )