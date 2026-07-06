from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# Кнопка "Размер детали"
# =========================
@router.message(F.text == "📏 Размер детали")
async def contour_size(message: Message):

    u = user(message.from_user.id)
    u.screen = "size"

    await message.answer(
        "Введите размеры детали.\n\n"
        "Формат:\n"
        "X Y Z\n\n"
        "Например:\n"
        "30 20 15"
    )


# =========================
# Ввод размеров
# =========================
@router.message(lambda m: len(m.text.split()) == 3)
async def contour_size_input(message: Message):

    u = user(message.from_user.id)

    if u.screen != "size":
        return

    try:

        x, y, z = map(float, message.text.split())

    except ValueError:

        await message.answer(
            "Ошибка.\n\n"
            "Введите размеры в формате:\n"
            "30 20 15"
        )
        return

    u.size_x = x
    u.size_y = y
    u.size_z = z

    u.screen = "contour"

    await message.answer(
        f"✅ Размер сохранён\n\n"
        f"X = {x}\n"
        f"Y = {y}\n"
        f"Z = {z}",
        reply_markup=contour_menu()
    )