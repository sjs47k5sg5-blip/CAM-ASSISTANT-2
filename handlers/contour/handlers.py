from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from .states import ContourWizard

router = Router()


# ==========================================
# ОТРИСОВКА ГЛАВНОГО МЕНЮ
# ==========================================

async def render_menu(state: FSMContext):

    data = await state.get_data()

    def status(value):
        return "✅" if value else "❌"

    text = (
        "📐 <b>КОНТУР</b>\n\n"

        f"{status(data.get('size_x'))} Размер детали\n"
        f"{status(data.get('material'))} Материал\n"
        f"{status(data.get('zero'))} Ноль детали\n"
        f"{status(data.get('zero_z'))} Ноль Z\n"
        f"{status(data.get('tool_diameter'))} Инструмент\n"

        f"{status(True)} Обработка углов\n"
        f"{status(True)} Припуск\n\n"

        "Выберите параметр:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📏 Размер детали",
                    callback_data="size"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🧱 Материал",
                    callback_data="material"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📍 Ноль детали",
                    callback_data="zero"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📍 Ноль Z",
                    callback_data="zero_z"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚙ Обработка углов",
                    callback_data="corner"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📉 Припуск",
                    callback_data="allowance"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔧 Инструмент",
                    callback_data="tool"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data="ready"
                )
            ]

        ]
    )

    return text, keyboard


# ==========================================
# РАЗМЕР ДЕТАЛИ
# ==========================================

@router.callback_query(F.data == "size")
async def size_click(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(ContourWizard.size)

    await callback.message.answer(
        "📏 Введите размеры детали.\n\n"
        "Формат:\n"
        "<b>X Y Z</b>\n\n"
        "Например:\n"
        "<code>30 20 15</code>",
        parse_mode="HTML"
    )

    await callback.answer()


# ==========================================
# ВВОД РАЗМЕРОВ
# ==========================================

@router.message(ContourWizard.size)
async def size_input(
    message: Message,
    state: FSMContext
):

    try:

        values = message.text.replace(",", ".").split()

        if len(values) != 3:
            raise ValueError

        x = float(values[0])
        y = float(values[1])
        z = float(values[2])

    except Exception:

        await message.answer(
            "❌ Неверный формат.\n\n"
            "Введите:\n"
            "<code>30 20 15</code>",
            parse_mode="HTML"
        )

        return

    await state.update_data(

        size_x=x,
        size_y=y,
        size_z=z

    )

    await state.set_state(ContourWizard.menu)

    text, kb = await render_menu(state)

    await message.answer(

        "✅ Размер детали сохранён."

    )

    await message.answer(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )


# ==========================================
# МАТЕРИАЛ
# ==========================================

@router.callback_query(F.data == "material")
async def material_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🟦 Алюминий",
                    callback_data="mat_ALUMINUM"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬛ Сталь",
                    callback_data="mat_STEEL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🟨 Латунь",
                    callback_data="mat_BRASS"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🟧 Медь",
                    callback_data="mat_COPPER"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "🧱 <b>Материал</b>\n\n"
        "Выберите материал.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ МАТЕРИАЛ
# ==========================================

@router.callback_query(F.data.startswith("mat_"))
async def material_save(
    callback: CallbackQuery,
    state: FSMContext
):

    material = callback.data.replace("mat_", "")

    await state.update_data(
        material=material
    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await state.set_state(ContourWizard.menu)

    await callback.answer()


# ==========================================
# НАЗАД
# ==========================================

@router.callback_query(F.data == "back_menu")
async def back_menu(
    callback: CallbackQuery,
    state: FSMContext
):

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await state.set_state(ContourWizard.menu)

    await callback.answer()


# ==========================================
# НОЛЬ ДЕТАЛИ
# ==========================================

@router.callback_query(F.data == "zero")
async def zero_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎯 Центр",
                    callback_data="zero_CENTER"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↖ Левый верхний",
                    callback_data="zero_TL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↗ Правый верхний",
                    callback_data="zero_TR"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↙ Левый нижний",
                    callback_data="zero_BL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↘ Правый нижний",
                    callback_data="zero_BR"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "📍 <b>Ноль детали</b>\n\n"
        "Выберите положение нуля.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ НОЛЬ
# ==========================================

@router.callback_query(F.data.startswith("zero_"))
async def zero_save(
    callback: CallbackQuery,
    state: FSMContext
):

    zero = callback.data.replace("zero_", "")

    await state.update_data(
        zero=zero
    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await state.set_state(ContourWizard.menu)

    await callback.answer()


# ==========================================
# НОЛЬ ПО Z
# ==========================================

@router.callback_query(F.data == "zero_z")
async def zero_z_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="⬆ Верх детали",
                    callback_data="zeroz_TOP"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬇ Низ детали",
                    callback_data="zeroz_BOTTOM"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "📍 <b>Ноль по Z</b>\n\n"
        "Выберите положение нуля по оси Z.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ НОЛЬ Z
# ==========================================

@router.callback_query(F.data.startswith("zeroz_"))
async def zero_z_save(
    callback: CallbackQuery,
    state: FSMContext
):

    zero_z = callback.data.replace("zeroz_", "")

    await state.update_data(
        zero_z=zero_z
    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await state.set_state(ContourWizard.menu)

    await callback.answer()


# ==========================================
# ОБРАБОТКА УГЛОВ
# ==========================================

@router.callback_query(F.data == "corner")
async def corner_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🔵 Радиус",
                    callback_data="corner_RADIUS"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔶 Фаска",
                    callback_data="corner_CHAMFER"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬜ Острые углы",
                    callback_data="corner_SHARP"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "⚙ <b>Обработка углов</b>\n\n"
        "Выберите тип обработки.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# ВЫБОР ТИПА
# ==========================================

@router.callback_query(F.data.startswith("corner_"))
async def corner_type(
    callback: CallbackQuery,
    state: FSMContext
):

    corner = callback.data.replace("corner_", "")

    # Острые углы -- сразу сохраняем
    if corner == "SHARP":

        await state.update_data(

            corner_type="SHARP",
            corner_select="ALL",
            corner_value=0

        )

        text, kb = await render_menu(state)

        await callback.message.edit_text(

            text,

            parse_mode="HTML",

            reply_markup=kb

        )

        await callback.answer()

        return

    await state.update_data(
        corner_type=corner
    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Все углы",
                    callback_data="cornerpos_ALL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↖ Левый верхний",
                    callback_data="cornerpos_TL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↗ Правый верхний",
                    callback_data="cornerpos_TR"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↙ Левый нижний",
                    callback_data="cornerpos_BL"
                )
            ],

            [
                InlineKeyboardButton(
                    text="↘ Правый нижний",
                    callback_data="cornerpos_BR"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="corner"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "Выберите углы для обработки.",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# ВЫБОР УГЛОВ
# ==========================================

@router.callback_query(F.data.startswith("cornerpos_"))
async def corner_position(
    callback: CallbackQuery,
    state: FSMContext
):

    position = callback.data.replace("cornerpos_", "")

    await state.update_data(
        corner_select=position
    )

    await state.set_state(ContourWizard.corner_value)

    await callback.message.answer(

        "Введите размер радиуса/фаски (мм)\n\n"
        "Например:\n"
        "<code>2</code>",

        parse_mode="HTML"

    )

    await callback.answer()


# ==========================================
# ВВОД РАЗМЕРА
# ==========================================

@router.message(ContourWizard.corner_value)
async def corner_value_input(
    message: Message,
    state: FSMContext
):

    try:

        value = float(
            message.text.replace(",", ".")
        )

        if value < 0:
            raise ValueError

    except Exception:

        await message.answer(

            "❌ Неверное значение.\n\n"
            "Введите число.\n\n"
            "Например:\n"
            "<code>2</code>",

            parse_mode="HTML"

        )

        return

    await state.update_data(

        corner_value=value

    )

    await state.set_state(
        ContourWizard.menu
    )

    text, kb = await render_menu(state)

    await message.answer(

        f"✅ Размер сохранён: {value} мм"

    )

    await message.answer(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )


# ==========================================
# ПРИПУСК
# ==========================================

@router.callback_query(F.data == "allowance")
async def allowance_click(
    callback: CallbackQuery,
    state: FSMContext
):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="0 мм",
                    callback_data="allow_0"
                )
            ],

            [
                InlineKeyboardButton(
                    text="0.2 мм",
                    callback_data="allow_0.2"
                )
            ],

            [
                InlineKeyboardButton(
                    text="0.5 мм",
                    callback_data="allow_0.5"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "📉 <b>Припуск</b>\n\n"
        "Выберите величину припуска.",

        parse_mode="HTML",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# СОХРАНИТЬ ПРИПУСК
# ==========================================

@router.callback_query(F.data.startswith("allow_"))
async def allowance_save(
    callback: CallbackQuery,
    state: FSMContext
):

    allowance = float(
        callback.data.replace("allow_", "")
    )

    await state.update_data(
        allowance=allowance
    )

    # если припуска нет
    if allowance == 0:

        await state.update_data(

            finish_pass=False,
            finish_tool=False

        )

        text, kb = await render_menu(state)

        await callback.message.edit_text(

            text,

            parse_mode="HTML",

            reply_markup=kb

        )

        await callback.answer()

        return

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="finish_yes"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="finish_no"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "Выполнять чистовой проход?",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# ЧИСТОВОЙ ПРОХОД
# ==========================================

@router.callback_query(F.data == "finish_no")
async def finish_no(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(

        finish_pass=False,
        finish_tool=False

    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await callback.answer()


@router.callback_query(F.data == "finish_yes")
async def finish_yes(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_pass=True
    )

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🔧 Тем же инструментом",
                    callback_data="finish_same"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🛠 Другим инструментом",
                    callback_data="finish_other"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "Как выполнить чистовой проход?",

        reply_markup=keyboard

    )

    await callback.answer()


# ==========================================
# ИНСТРУМЕНТ ЧИСТОВОГО ПРОХОДА
# ==========================================

@router.callback_query(F.data == "finish_same")
async def finish_same(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_tool=False
    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await callback.answer()


@router.callback_query(F.data == "finish_other")
async def finish_other(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        finish_tool=True
    )

    text, kb = await render_menu(state)

    await callback.message.edit_text(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )

    await callback.answer()


# ==========================================
# ИНСТРУМЕНТ
# ==========================================

@router.callback_query(F.data == "tool")
async def tool_click(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(ContourWizard.tool)

    await callback.message.answer(

        "🔧 <b>Инструмент</b>\n\n"
        "Введите номер инструмента и диаметр.\n\n"
        "Формат:\n"
        "<code>3 10</code>\n\n"
        "где\n"
        "3 -- номер инструмента (T3)\n"
        "10 -- диаметр фрезы (Ø10 мм)",

        parse_mode="HTML"

    )

    await callback.answer()


# ==========================================
# ВВОД ИНСТРУМЕНТА
# ==========================================

@router.message(ContourWizard.tool)
async def tool_input(
    message: Message,
    state: FSMContext
):

    try:

        values = message.text.replace(",", ".").split()

        if len(values) != 2:
            raise ValueError

        tool_number = int(values[0])
        tool_diameter = float(values[1])

        if tool_number <= 0:
            raise ValueError

        if tool_diameter <= 0:
            raise ValueError

    except Exception:

        await message.answer(

            "❌ Неверный формат.\n\n"
            "Введите:\n"
            "<code>3 10</code>",

            parse_mode="HTML"

        )

        return

    await state.update_data(

        tool_number=tool_number,
        tool_diameter=tool_diameter

    )

    await state.set_state(
        ContourWizard.menu
    )

    text, kb = await render_menu(state)

    await message.answer(

        f"✅ Инструмент сохранён\n\n"
        f"T{tool_number}\n"
        f"Ø{tool_diameter} мм"

    )

    await message.answer(

        text,

        parse_mode="HTML",

        reply_markup=kb

    )


# ==========================================
# ГОТОВО
# ==========================================

@router.callback_query(F.data == "ready")
async def ready_click(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    errors = []

    if not data.get("size_x"):
        errors.append("• Размер детали")

    if not data.get("material"):
        errors.append("• Материал")

    if not data.get("zero"):
        errors.append("• Ноль детали")

    if not data.get("zero_z"):
        errors.append("• Ноль по Z")

    if not data.get("tool_diameter"):
        errors.append("• Инструмент")

    if errors:

        await callback.message.answer(

            "❌ Заполнены не все параметры.\n\n"
            "Необходимо заполнить:\n\n"
            + "\n".join(errors)

        )

        await callback.answer()

        return

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="▶ Сгенерировать G-код",
                    callback_data="generate"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="back_menu"
                )
            ]

        ]

    )

    await callback.message.edit_text(

        "✅ Все параметры заполнены.\n\n"
        "Можно приступать к генерации программы.",

        reply_markup=keyboard

    )

    await state.set_state(
        ContourWizard.ready
    )

    await callback.answer()