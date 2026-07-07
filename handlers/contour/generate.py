from io import BytesIO

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from services.cam_engine import contour
from .states import ContourWizard

router = Router()


@router.callback_query(
    ContourWizard.ready,
    F.data == "generate"
)
async def generate_gcode(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    try:

        gcode = contour(

            x=data["size_x"],
            y=data["size_y"],

            depth=data["size_z"],

            stepdown=2,

            tool=data["tool_number"],

            zero=data["zero"],

            allowance=data["allowance"],

            step=1,

            corner_type=data["corner_type"],

            corner_value=data["corner_value"]

        )

    except Exception as e:

        await callback.message.answer(

            f"Ошибка генерации:\n\n{e}"

        )

        await callback.answer()

        return

    file = BufferedInputFile(

        gcode.encode(),

        filename="Contour.nc"

    )

    await callback.message.answer_document(

        file,

        caption="✅ G-код успешно создан."

    )

    await callback.answer()