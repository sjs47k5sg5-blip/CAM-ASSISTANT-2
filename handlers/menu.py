from aiogram import Router, F
from aiogram.types import Message
from keyboards.cam_menu import cam_menu

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🚀 CAM CORE READY", reply_markup=cam_menu)

@router.message(F.text == "CAM")
async def cam(message: Message):
    await message.answer("📐 CAM открыт", reply_markup=cam_menu)

@router.message(F.text == "Контур")
async def contour_btn(message: Message):
    await message.answer("📐 Контур выбран")

@router.message(F.text == "Карман")
async def pocket_btn(message: Message):
    await message.answer("🟦 Карман выбран")

@router.message(F.text == "Справочник")
async def manual(message: Message):
    await message.answer("📚 Справочник")