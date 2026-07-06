from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

from keyboards.contour_menu import contour_menu

router = Router()


def user(uid: int):

    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()

    return CAM_DB[uid]


@router.message(F.text == "📐 Контур")
async def contour(message: Message):

    u = user(message.from_user.id)

    u.screen = "contour"

    await message.answer(
        "📐 Контур\n\n"
        "Введите параметры обработки.",
        reply_markup=contour_menu()
    )