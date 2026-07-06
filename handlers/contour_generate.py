from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from handlers.cam_state import CAM_DB
from keyboards.finish_menu import finish_menu
from keyboards.contour_menu import contour_menu

from services.Cam_engine import contour

router = Router()


def user(uid: int):
    return CAM_DB[uid]


# ======================================
# ГОТОВО
# ======================================

@router.message(F.text == "✅ Готово")
async def ready(message: Message):

    u = user(message.from_user.id)

    errors = []

    if u.size_x <= 0:
        errors.append("• Размер детали")

    if u.material == "":
        errors.append("• Материал")

    if u.tool_diameter <= 0:
        errors.append("• Инструмент")

    if errors:

        await message.answer(
            "Не заполнены параметры:\n\n"
            + "\n".join(errors),
            reply_markup=contour_menu()
        )

        return

    u.ready = True

    await message.answer(
        "Все параметры заполнены.\n\n"
        "Нажмите кнопку ниже.",
        reply_markup=finish_menu()
    )


# ======================================
# ГЕНЕРАЦИЯ
# ======================================

@router.message(F.text == "▶️ Сгенерировать G-код")
async def generate(message: Message):

    u = user(message.from_user.id)

    if not u.ready:

        await message.answer(
            "Сначала заполните параметры."
        )

        return

    gcode = contour(

        x=u.size_x,
        y=u.size_y,

        depth=u.size_z,

        stepdown=2,

        tool=u.tool_diameter,

        zero=u.zero,

        allowance=u.allowance,

        step=0,

        corner_type=u.corner_type,

        corner_value=u.corner_value
    )

    filename = "Contour.nc"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(gcode)

    await message.answer_document(
        FSInputFile(filename),
        caption="Готовый G-код"
    )