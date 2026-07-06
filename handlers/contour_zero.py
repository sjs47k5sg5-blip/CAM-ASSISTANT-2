from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.zero_menu import zero_menu
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    if uid not in CAM_DB:
        from handlers.cam_state import CamState
        CAM_DB[uid] = CamState()

    return CAM_DB[uid]


@router.message(F.text == "📍 Ноль детали")
async def zero_start(message: Message):

    u = user(message.from_user.id)

    u.screen = "zero"

    await message.answer(
        "Выберите ноль детали",
        reply_markup=zero_menu()
    )


@router.message(F.text == "Центр")
async def zero_center(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.zero = "CENTER"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль детали: Центр",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Левый верхний")
async def zero_left_top(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.zero = "TL"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль детали: Левый верхний",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Правый верхний")
async def zero_right_top(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.zero = "TR"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль детали: Правый верхний",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Левый нижний")
async def zero_left_bottom(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.zero = "BL"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль детали: Левый нижний",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Правый нижний")
async def zero_right_bottom(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.zero = "BR"
    u.screen = "contour"

    await message.answer(
        "✅ Ноль детали: Правый нижний",
        reply_markup=contour_menu()
    )


@router.message(F.text == "⬅️ Назад")
async def zero_back(message: Message):

    u = user(message.from_user.id)

    if u.screen != "zero":
        return

    u.screen = "contour"

    await message.answer(
        "Параметры обработки",
        reply_markup=contour_menu()
    )