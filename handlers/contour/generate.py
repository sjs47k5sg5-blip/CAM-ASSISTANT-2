from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from services.cam_engine.engine import generate_contour
from services.cam_engine.project_manager import ProjectManager
from services.cam_engine.builders.rectangle_builder import RectangleBuilder

router = Router()


@router.callback_query(F.data == "generate")
async def generate(
    callback: CallbackQuery,
    state: FSMContext,
):

    data = await state.get_data()

    project = ProjectManager.new_project()

    project.contour = RectangleBuilder().build(
        project.workpiece.x,
        project.workpiece.y,
        project.workpiece.zero,
    )

    # =====================================
    # ЗАГОТОВКА
    # =====================================

    project.workpiece.x = data.get("size_x", 0.0)
    project.workpiece.y = data.get("size_y", 0.0)
    project.workpiece.z = data.get("size_z", 0.0)

    project.workpiece.zero = data.get("zero", "CENTER")
    project.workpiece.zero_z = data.get("zero_z", "TOP")

    # =====================================
    # МАТЕРИАЛ
    # =====================================

    project.material.name = data.get("material", "Steel")

    # =====================================
    # ИНСТРУМЕНТ
    # =====================================

    project.tool.number = data.get("tool_number", 1)
    project.tool.length_offset = project.tool.number
    project.tool.diameter = data.get("tool_diameter", 10.0)

    # =====================================
    # УГЛЫ
    # =====================================

    project.corner.kind = data.get(
        "corner_type",
        "SHARP",
    )

    project.corner.position = data.get(
        "corner_select",
        "ALL",
    )

    project.corner.value = float(
        data.get(
            "corner_value",
            0.0,
        )
    )

    # =====================================
    # ЧИСТОВОЙ
    # =====================================

    project.finish.allowance = data.get("allowance") or 0.0
    project.finish.enabled = data.get("finish_pass", False)
    project.finish.another_tool = data.get("finish_tool", False)

    # =====================================
    # ОБРАБОТКА
    # =====================================

    project.machining.direction = data.get(
        "cut_direction",
        "CLIMB",
    )

    project.machining.roughing = data.get(
        "roughing_enabled",
        False,
    )

    project.machining.stepover = data.get(
        "roughing_stepover",
        0.6,
    )

    project.machining.step_z = data.get(
        "step_z",
        2.0,
    )

    # =====================================
    # ГЕНЕРАЦИЯ
    # =====================================

    try:

        gcode = generate_contour(project)

    except Exception as e:

        await callback.message.answer(
            f"❌ Ошибка генерации\n\n{e}"
        )

        await callback.answer()

        return

    await callback.message.answer_document(

        BufferedInputFile(
            gcode.encode("utf-8"),
            filename="Contour.nc",
        ),

        caption="✅ G-код успешно создан.",

    )

    await callback.answer()