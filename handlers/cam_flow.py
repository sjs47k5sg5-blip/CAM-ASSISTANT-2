from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState
from keyboards.cam_wizard import wizard_type

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


@router.message(F.text == "📐 Контур")
@router.message(F.text == "🔵 Радиус")
@router.message(F.text == "📏 Фаска")
async def mode(message: Message):

    u = state(message.from_user.id)
    u.mode = message.text

    await message.answer("✔ Режим выбран\nВведите инструмент:")


@router.message(F.text.regexp(r"^\d+$"))
async def tool(message: Message):

    u = state(message.from_user.id)
    u.tool = int(message.text)
    u.step = 1

    await message.answer("✔ Инструмент сохранён")


@router.message(F.text.in_(["Центр", "ЛВ", "ПВ", "ЛН", "ПН"]))
async def zero(message: Message):

    u = state(message.from_user.id)
    u.zero = message.text
    u.step = 2

    await message.answer("✔ Ноль установлен")


@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer("↩ CAM", reply_markup=wizard_type())


@router.message(F.text == "Сгенерировать")
async def generate(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=40,
        y=30,
        depth=u.depth,
        stepdown=u.stepdown,
        tool=u.tool,
        zero=u.zero,
        allowance=u.allowance,
        step=0,
        corner_type=u.mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")