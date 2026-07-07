from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu
from keyboards.milling_menu import milling_menu
from keyboards.drilling_menu import drilling_menu

router = Router()


# ==========================================
# START
# ==========================================

@router.message(F.text == "/start")
async def start(message: Message):

    await message.answer(

        "🤖 CAM Assistant V5\n\n"
        "Выберите раздел.",

        reply_markup=main_menu()

    )


# ==========================================
# ПРОЕКТЫ
# ==========================================

@router.message(F.text == "📁 Проекты")
async def projects(message: Message):

    await message.answer(

        "📁 Раздел находится в разработке.",

        reply_markup=main_menu()

    )


# ==========================================
# ФРЕЗЕРОВКА
# ==========================================

@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):

    await message.answer(

        "⚙ Выберите операцию.",

        reply_markup=milling_menu()

    )


# ==========================================
# ОТВЕРСТИЯ
# ==========================================

@router.message(F.text == "🕳 Обработка отверстий")
async def holes(message: Message):

    await message.answer(

        "🕳 Выберите операцию.",

        reply_markup=drilling_menu()

    )


# ==========================================
# ПОСОБИЕ
# ==========================================

@router.message(F.text == "📚 Пособие")
async def handbook(message: Message):

    await message.answer(

        "📚 Раздел находится в разработке."

    )


# ==========================================
# О ПРОГРАММЕ
# ==========================================

@router.message(F.text == "ℹ О программе")
async def about(message: Message):

    await message.answer(

        "CAM Assistant V5\n"
        "Промышленный CAM для ЧПУ."

    )


# ==========================================
# НАЗАД
# ==========================================

@router.message(F.text == "⬅ Назад")
async def back(message: Message):

    await message.answer(

        "Главное меню.",

        reply_markup=main_menu()

    )