from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def number_input(
    message: Message,
    state: FSMContext,
):

    data = await state.get_data()

    parameter = data.get("input_parameter")

    if parameter is None:
        return

    try:

        value = float(
            message.text.replace(",", ".")
        )

    except ValueError:

        await message.answer(
            "❌ Введите число."
        )

        return

    # сохраняем значение

    await state.update_data(

        **{

            parameter: value,

            "input_parameter": None,

        }

    )

    await message.answer(

        f"✅ Значение сохранено: {value}"

    )

    # Здесь позже будет переход
    # на следующий шаг мастера