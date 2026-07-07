from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .states import ContourWizard
from .menu import render_menu

router = Router()


# ==========================================
# ЗАПУСК МАСТЕРА
# ==========================================

@router.message(F.text == "📐 Контур")
async def contour_start(
    message: Message,
    state: FSMContext,
):

    await state.clear()

    await state.set_state(ContourWizard.menu)

    await state.update_data(

        # Размер детали
        size_x=None,
        size_y=None,
        size_z=None,

        # Материал
        material=None,

        # Ноль
        zero=None,
        zero_z=None,

        # Инструмент
        tool_number=None,
        tool_diameter=None,

        # ===== Обработка =====

        processing_ready=False,

        roughing_enabled=False,

        step_z=2.0,

        roughing_stepover=0.6,

        cut_direction="CLIMB",

        allowance=0.0,

        finish_pass=False,

        finish_tool=False,

        corner_type="SHARP",

        corner_select="ALL",

        corner_value=0.0,

    )

    text, kb = await render_menu(state)

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=kb,
    )


# ==========================================
# ROUTERS
# ==========================================

from .menu import router as menu_router
from .size import router as size_router
from .material import router as material_router
from .zero import router as zero_router
from .tool import router as tool_router
from .processing.router import router as processing_router
from .ready import router as ready_router
from .generate import router as generate_router

router.include_router(menu_router)
router.include_router(size_router)
router.include_router(material_router)
router.include_router(zero_router)
router.include_router(tool_router)
router.include_router(processing_router)
router.include_router(ready_router)
router.include_router(generate_router)