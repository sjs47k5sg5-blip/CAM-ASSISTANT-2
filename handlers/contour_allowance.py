from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB

from keyboards.allowance_menu import allowance_menu
from keyboards.finish_pass_menu import finish_pass_menu
from keyboards.finish_tool_menu import finish_tool_menu
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# ПРИПУСК
# =========================

@router.message(F.text == "📉 Припуск")
async def allowance(message: Message):

    u = user(message.from_user.id)
    u.screen = "allowance"

    await message.answer(
        "Выберите припуск",
        reply_markup=allowance_menu()
    )


# =========================
# 0
# =========================

@router.message(F.text == "0")
async def allowance0(message: Message):

    u = user(message.from_user.id)

    if u.screen != "allowance":
        return

    u.allowance = 0
    u.finish_pass = False
    u.finish_tool = False

    u.screen = "contour"

    await message.answer(
        "✅ Припуск = 0",
        reply_markup=contour_menu()
    )


# =========================
# 0.2
# =========================

@router.message(F.text == "0.2")
async def allowance02(message: Message):

    u = user(message.from_user.id)

    if u.screen != "allowance":
        return

    u.allowance = 0.2
    u.screen = "finish_pass"

    await message.answer(
        "Выполнить чистовой проход?",
        reply_markup=finish_pass_menu()
    )


# =========================
# 0.5
# =========================

@router.message(F.text == "0.5")
async def allowance05(message: Message):

    u = user(message.from_user.id)

    if u.screen != "allowance":
        return

    u.allowance = 0.5
    u.screen = "finish_pass"

    await message.answer(
        "Выполнить чистовой проход?",
        reply_markup=finish_pass_menu()
    )


# =========================
# ЧИСТОВОЙ ПРОХОД
# =========================

@router.message(F.text == "Да")
async def finish_yes(message: Message):

    u = user(message.from_user.id)

    if u.screen != "finish_pass":
        return

    u.finish_pass = True
    u.screen = "finish_tool"

    await message.answer(
        "Каким инструментом?",
        reply_markup=finish_tool_menu()
    )


@router.message(F.text == "Нет")
async def finish_no(message: Message):

    u = user(message.from_user.id)

    if u.screen != "finish_pass":
        return

    u.finish_pass = False
    u.finish_tool = False
    u.screen = "contour"

    await message.answer(
        "✅ Припуск сохранён",
        reply_markup=contour_menu()
    )


# =========================
# ИНСТРУМЕНТ
# =========================

@router.message(F.text == "Тем же инструментом")
async def same_tool(message: Message):

    u = user(message.from_user.id)

    if u.screen != "finish_tool":
        return

    u.finish_tool = False
    u.screen = "contour"

    await message.answer(
        "✅ Чистовой проход тем же инструментом",
        reply_markup=contour_menu()
    )


@router.message(F.text == "Другим инструментом")
async def other_tool(message: Message):

    u = user(message.from_user.id)

    if u.screen != "finish_tool":
        return

    u.finish_tool = True
    u.screen = "contour"

    await message.answer(
        "✅ Будет использован другой инструмент",
        reply_markup=contour_menu()
    )