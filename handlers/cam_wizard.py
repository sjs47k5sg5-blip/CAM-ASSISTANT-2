from aiogram import Router, F
from aiogram.types import Message

from keyboards.cam_wizard import (
    wizard_start,
    wizard_type,
    wizard_zero,
    wizard_corners,
    wizard_scope,
    wizard_params
)

router = Router()

# =========================
# START WIZARD
# =========================
@router.message(F.text == "🚀 Начать CAM")
async def start_wizard(message: Message):
    await message.answer("Шаг 1: выбери тип обработки", reply_markup=wizard_type())


# =========================
# STEP ROUTING (SIMPLE STATELESS VERSION)
# =========================
@router.message(F.text == "📐 Контур")
@router.message(F.text == "🔵 Радиус")
@router.message(F.text == "📏 Фаска")
async def step_type(message: Message):
    await message.answer("Шаг 2: выбери ноль детали", reply_markup=wizard_zero())


@router.message(F.text.in_(["🎯 Центр", "↖ ЛВ угол", "↗ ПВ угол", "↙ ЛН угол", "↘ ПН угол"]))
async def step_zero(message: Message):
    await message.answer("Шаг 3: тип углов", reply_markup=wizard_corners())


@router.message(F.text.in_(["⬜ Острые", "⭕ Радиус", "📐 Фаска"]))
async def step_corners(message: Message):
    await message.answer("Шаг 4: какие углы обрабатывать", reply_markup=wizard_scope())


@router.message(F.text.in_(["Все углы", "Внешние", "Внутренние", "Ручной выбор"]))
async def step_scope(message: Message):
    await message.answer("Шаг 5: параметры CAM", reply_markup=wizard_params())


@router.message(F.text == "🧪 Симуляция")
async def simulation(message: Message):
    await message.answer("Запуск симуляции...")


@router.message(F.text == "✅ Сгенерировать")
async def generate(message: Message):
    await message.answer("Генерация G-code...")