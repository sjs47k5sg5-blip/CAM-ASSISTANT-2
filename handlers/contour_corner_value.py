from aiogram import Router
from aiogram.types import Message

from handlers.cam_state import CAM_DB
from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# =========================
# ВВОД ЗНАЧЕНИЯ РАДИУСА / ФАСКИ
# =========================

@router.message()
async def corner_value(message: Message):

    u = user(message.from_user.id)

    if u.screen != "corner_value":
        return

    try:
        value = float(message.text.replace(",", "."))

        if value < 0:
            raise ValueError

    except ValueError:

        await message.answer(
            "Введите корректное значение в миллиметрах.\n\n"
            "Например:\n"
            "2\n"
            "0.5"
        )
        return

    u.corner_value = value

    u.screen = "contour"

    text = (
        "✅ Параметры углов сохранены\n\n"
        f"Тип: {'Радиус' if u.corner_type == 'RADIUS' else 'Фаска'}\n"
        f"Углы: {u.corner_select}\n"
        f"Размер: {u.corner_value} мм"
    )

    await message.answer(
        text,
        reply_markup=contour_menu()
    )