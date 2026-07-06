from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.corner_menu import corner_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# ОБРАБОТКА УГЛОВ
# =========================

@router.message(F.text == "⚙ Обработка углов")
async def corner_menu_handler(message: Message):

    u = user(message.from_user.id)
    u.screen = "corner"

    await message.answer(
        "Выберите тип обработки углов",
        reply_markup=corner_menu()
    )


# =========================
# РАДИУС
# =========================

@router.message(F.text == "Радиус")
async def radius(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner":
        return

    u.corner_type = "RADIUS"
    u.screen = "corner_select"

    from keyboards.corner_select_menu import corner_select_menu

    await message.answer(
        "Какие углы обработать?",
        reply_markup=corner_select_menu()
    )


# =========================
# ФАСКА
# =========================

@router.message(F.text == "Фаска")
async def chamfer(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner":
        return

    u.corner_type = "CHAMFER"
    u.screen = "corner_select"

    from keyboards.corner_select_menu import corner_select_menu

    await message.answer(
        "Какие углы обработать?",
        reply_markup=corner_select_menu()
    )


# =========================
# ОСТРЫЕ
# =========================

@router.message(F.text == "Острые углы")
async def sharp(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner":
        return

    u.corner_type = "SHARP"
    u.corner_select = "ALL"
    u.corner_value = 0
    u.screen = "contour"

    from keyboards.contour_menu import contour_menu

    await message.answer(
        "✅ Острые углы выбраны",
        reply_markup=contour_menu()
    )


# =========================
# НАЗАД
# =========================

@router.message(F.text == "⬅️ Назад")
async def back(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner":
        return

    u.screen = "contour"

    from keyboards.contour_menu import contour_menu

    await message.answer(
        "Введите параметры обработки",
        reply_markup=contour_menu()
    )