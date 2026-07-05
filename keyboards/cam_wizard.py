from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# WIZARD START
# =========================
def wizard_start():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Начать CAM")]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 1: TYPE
# =========================
def wizard_type():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📐 Контур"),
                KeyboardButton(text="🔵 Радиус"),
                KeyboardButton(text="📏 Фаска")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 2: ZERO
# =========================
def wizard_zero():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎯 Центр"),
                KeyboardButton(text="↖ ЛВ угол")
            ],
            [
                KeyboardButton(text="↗ ПВ угол"),
                KeyboardButton(text="↙ ЛН угол"),
                KeyboardButton(text="↘ ПН угол")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 3: CORNERS
# =========================
def wizard_corners():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⬜ Острые"),
                KeyboardButton(text="⭕ Радиус"),
                KeyboardButton(text="📐 Фаска")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 4: CORNER SCOPE
# =========================
def wizard_scope():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Все углы"),
                KeyboardButton(text="Внешние")
            ],
            [
                KeyboardButton(text="Внутренние"),
                KeyboardButton(text="Ручной выбор")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 5: PARAMETERS
# =========================
def wizard_params():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📏 Припуск"),
                KeyboardButton(text="🔧 Инструмент")
            ],
            [
                KeyboardButton(text="📐 Радиус/Фаска"),
                KeyboardButton(text="⚙ Stepdown")
            ],
            [
                KeyboardButton(text="🧪 Симуляция"),
                KeyboardButton(text="✅ Сгенерировать")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )