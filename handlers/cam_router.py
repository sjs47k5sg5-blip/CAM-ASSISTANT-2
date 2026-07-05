from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


# =========================
# 📐 КОНТУР
# =========================
@router.callback_query(F.data == "cam_contour")
async def contour(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("📐 Контур выбран")


# =========================
# ⬜ КАРМАН
# =========================
@router.callback_query(F.data == "cam_pocket")
async def pocket(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("⬜ Карман выбран")