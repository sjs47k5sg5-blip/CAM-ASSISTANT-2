from io import BytesIO

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    BufferedInputFile,
)
from aiogram.fsm.context import FSMContext

from services.cam_engine.engine import generate_contour
from services.cam_engine.project_manager import ProjectManager

router = Router()


@router.callback_query(F.data == "generate")
async def generate(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    project = ProjectManager.new_project()

    # -----------------------------------
    # Заготовка
    # -----------------------------------

    project.workpiece.x = data["size_x"]
    project.workpiece.y = data["size_y"]
    project.workpiece.z = data["size_z"]

    project.workpiece.zero = data["zero"]
    project.workpiece.zero_z = data["zero_z"]

    # -----------------------------------
    # Материал
    # -----------------------------------

    project.material.name = data["material"]

    # -----------------------------------
    # Инструмент
    # -----------------------------------

    project.tool.number = data["tool_number"]
    project.tool.diameter = data["tool_diameter"]

    # -----------------------------------
    # Углы
    # -----------------------------------

    project.corner.kind = data["corner_type"]
    project.corner.position = data["corner_select"]
    project.corner.value = data["corner_value"]

    # -----------------------------------
    # Припуск
    # -----------------------------------

    project.finish.allowance = data["allowance"]
    project.finish.enabled = data["finish_pass"]
    project.finish.another_tool = data["finish_tool"]

    # -----------------------------------
    # Генерация
    # -----------------------------------

    try:

        gcode = generate_contour(project)

    except Exception as e:

        await callback.message.answer(

            f"❌ Ошибка генерации\n\n{e}"

        )

        await callback.answer()

        return

    file = BufferedInputFile(

        gcode.encode("utf-8"),

        filename="Contour.nc"

    )

    await callback.message.answer_document(

        file,

        caption="✅ G-код успешно создан."

    )

    await callback.answer()