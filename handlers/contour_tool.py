from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# ИНСТРУМЕНТ
# =========================

@router.message(F.text == "🔧 Инструмент")
async def tool(message: Message):

    u = user(message.from_user.id)
    u.screen = "tool"

    await message.answer(
        "Введите диаметр инструмента (мм)\n\n"
        "Например:\n"
        "10"
    )


# =========================
# ВВОД ДИАМЕТРА
# =========================

@router.message()
async def tool_value(message: Message):

    u = user(message.from_user.id)

    if u.screen != "tool":
        return

    try:
        d = float(message.text.replace(",", "."))

        if d <= 0:
            raise ValueError

    except ValueError:

        await message.answer(
            "Введите корректный диаметр.\n\n"
            "Например:\n"
            "10"
        )
        return

    u.tool_diameter = d
    u.screen = "contour"

    await message.answer(
        f"✅ Инструмент Ø{d} мм сохранён",
        reply_markup=contour_menu()
    )