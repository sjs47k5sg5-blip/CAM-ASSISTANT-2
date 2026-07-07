from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.contour_inline import contour_menu
from .states import ContourWizard

router = Router()


@router.message(F.text == "📐 Контур")
async def contour_start(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await state.set_state(ContourWizard.menu)

    await state.update_data(
        size_x=None,
        size_y=None,
        size_z=None,

        material=None,

        zero=None,
        zero_z=None,

        tool_number=1,
        tool_diameter=None,

        allowance=0,

        finish_pass=False,
        finish_tool=False,

        corner_type="SHARP",
        corner_select="ALL",
        corner_value=0,
    )

    await message.answer(
        "📐 <b>Контур</b>\n\n"
        "Введите параметры обработки.",
        parse_mode="HTML",
        reply_markup=contour_menu()
    )


# -----------------------------------------
# Подключаем внутренние роутеры
# -----------------------------------------

from .handlers import router as handlers_router
from .generate import router as generate_router

router.include_router(handlers_router)
router.include_router(generate_router)