from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.material_menu import material_menu
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# МАТЕРИАЛ
# =========================
@router.message(F.text == "🧱 Материал")
async def material(message: Message):

    u = user(message.from_user.id)
    u.screen = "material"

    await message.answer(
        "Выберите материал",
        reply_markup=material_menu()
    )


# =========================
# АЛЮМИНИЙ
# =========================
@router.message(F.text == "Алюминий")
async def alu(message: Message):

    u = user(message.from_user.id)

    if u.screen != "material":
        return

    u.material = "ALUMINUM"
    u.screen = "contour"

    await message.answer(
        "✅ Материал: Алюминий",
        reply_markup=contour_menu()
    )


# =========================
# СТАЛЬ
# =========================
@router.message(F.text == "Сталь")
async def steel(message: Message):

    u = user(message.from_user.id)

    if u.screen != "material":
        return

    u.material = "STEEL"
    u.screen = "contour"

    await message.answer(
        "✅ Материал: Сталь",
        reply_markup=contour_menu()
    )


# =========================
# ЛАТУНЬ
# =========================
@router.message(F.text == "Латунь")
async def brass(message: Message):

    u = user(message.from_user.id)

    if u.screen != "material":
        return

    u.material = "BRASS"
    u.screen = "contour"

    await message.answer(
        "✅ Материал: Латунь",
        reply_markup=contour_menu()
    )


# =========================
# МЕДЬ
# =========================
@router.message(F.text == "Медь")
async def copper(message: Message):

    u = user(message.from_user.id)

    if u.screen != "material":
        return

    u.material = "COPPER"
    u.screen = "contour"

    await message.answer(
        "✅ Материал: Медь",
        reply_markup=contour_menu()
    )


# =========================
# НАЗАД
# =========================
@router.message(F.text == "⬅️ Назад")
async def back(message: Message):

    u = user(message.from_user.id)

    if u.screen == "material":
        u.screen = "contour"

        await message.answer(
            "Параметры обработки",
            reply_markup=contour_menu()
        )