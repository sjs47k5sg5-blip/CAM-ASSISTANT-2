from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# ВСЕ УГЛЫ
# =========================

@router.message(F.text == "Все")
async def all_corner(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.corner_select = "ALL"
    u.screen = "corner_value"

    await message.answer(
        f"Введите {'радиус' if u.corner_type == 'RADIUS' else 'фаску'} в мм"
    )


# =========================
# ЛЕВЫЙ ВЕРХНИЙ
# =========================

@router.message(F.text == "Левый верхний")
async def tl(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.corner_select = "TL"
    u.screen = "corner_value"

    await message.answer(
        f"Введите {'радиус' if u.corner_type == 'RADIUS' else 'фаску'} в мм"
    )


# =========================
# ПРАВЫЙ ВЕРХНИЙ
# =========================

@router.message(F.text == "Правый верхний")
async def tr(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.corner_select = "TR"
    u.screen = "corner_value"

    await message.answer(
        f"Введите {'радиус' if u.corner_type == 'RADIUS' else 'фаску'} в мм"
    )


# =========================
# ЛЕВЫЙ НИЖНИЙ
# =========================

@router.message(F.text == "Левый нижний")
async def bl(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.corner_select = "BL"
    u.screen = "corner_value"

    await message.answer(
        f"Введите {'радиус' if u.corner_type == 'RADIUS' else 'фаску'} в мм"
    )


# =========================
# ПРАВЫЙ НИЖНИЙ
# =========================

@router.message(F.text == "Правый нижний")
async def br(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.corner_select = "BR"
    u.screen = "corner_value"

    await message.answer(
        f"Введите {'радиус' if u.corner_type == 'RADIUS' else 'фаску'} в мм"
    )


# =========================
# НАЗАД
# =========================

@router.message(F.text == "⬅️ Назад")
async def back(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_select":
        return

    u.screen = "corner"

    from keyboards.corner_menu import corner_menu

    await message.answer(
        "Выберите тип обработки углов",
        reply_markup=corner_menu()
    )