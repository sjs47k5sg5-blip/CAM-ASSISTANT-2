from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from .data import PROCESSING_STEPS
from ..ui import show_main_menu

router = Router()


# ==========================================
# ПОКАЗАТЬ ШАГ
# ==========================================

async def show_step(
    callback: CallbackQuery,
    state: FSMContext,
    index: int,
):

    if index >= len(PROCESSING_STEPS):

        await state.update_data(
            processing_ready=True
        )

        await show_main_menu(
            callback,
            state,
        )

        return

    step = PROCESSING_STEPS[index]

    await state.update_data(
        processing_index=index
    )

    keyboard = []

    row = []

    # ------------------------------
    # Choice
    # ------------------------------

    if step["type"] == "choice":

        for text, value in step["choices"]:

            row.append(

                InlineKeyboardButton(

                    text=text,

                    callback_data=f"proc:{index}:{value}"

                )

            )

            if len(row) == 2:

                keyboard.append(row)

                row = []

    # ------------------------------
    # Number
    # ------------------------------

    else:

        for text, value in step["values"]:

            row.append(

                InlineKeyboardButton(

                    text=text,

                    callback_data=f"proc:{index}:{value}"

                )

            )

            if len(row) == 2:

                keyboard.append(row)

                row = []

        if row:
            keyboard.append(row)

        keyboard.append(

            [

                InlineKeyboardButton(

                    text="✏️ Ввести своё значение",

                    callback_data=f"custom:{step['field']}"

                )

            ]

        )

    keyboard.append(

        [

            InlineKeyboardButton(

                text="⬅ Назад",

                callback_data="back_menu"

            )

        ]

    )

    progress = int((index + 1) / len(PROCESSING_STEPS) * 10)

    bar = "🟩" * progress + "⬜" * (10 - progress)

    await callback.message.edit_text(

        f"{step['title']}\n\n"

        f"Шаг {index+1} из {len(PROCESSING_STEPS)}\n\n"

        f"{bar}",

        parse_mode="HTML",

        reply_markup=InlineKeyboardMarkup(

            inline_keyboard=keyboard

        )

    )

    await callback.answer()


# ==========================================
# СТАРТ
# ==========================================

@router.callback_query(F.data == "processing")
async def processing_start(
    callback: CallbackQuery,
    state: FSMContext,
):

    await show_step(
        callback,
        state,
        0,
    )


# ==========================================
# СОХРАНИТЬ
# ==========================================

@router.callback_query(F.data.startswith("proc:"))
async def processing_save(
    callback: CallbackQuery,
    state: FSMContext,
):

    _, index, value = callback.data.split(":")

    index = int(index)

    step = PROCESSING_STEPS[index]

    # bool

    if value == "True":
        value = True

    elif value == "False":
        value = False

    else:

        try:

            value = float(value)

        except:

            pass

    await state.update_data(

        **{

            step["field"]: value

        }

    )

    await show_step(

        callback,

        state,

        index + 1,

    )