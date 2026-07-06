from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.zero_z_menu import zero_z_menu
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# НОЛЬ ПО Z
# =========================
@router.message(F.text == "📍 Ноль Z")
async def zero_z(message: Message):

    u = user(message.from_user.id)
    u.screen = "zero_z"

    await message.answer(
        "Выберите ноль по Z",
        reply_markup=zero_z_menu()
    )


@router.message(F.text == "Верх детали")
async def top(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero_z":
        return

    u.zero_z = "TOP"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль по Z: Верх детали",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Низ детали")
async def bottom(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero_z":
        return

    u.zero_z = "BOTTOM"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль по Z: Низ детали",
        reply_markup=contour_menu()
    )


@router.message(F.text == "⬅️ Назад")
async def back(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero_z":
        return

    u.screen = "contour"

    await message.answer(
        "Введите параметры обработки",
        reply_markup=contour_menu()
    )