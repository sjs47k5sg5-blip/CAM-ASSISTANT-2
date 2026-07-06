from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# STEP 1 -- ТОЛЬКО КОНТУР
# =========================
def wizard_type():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📐 Контур")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 2 -- НОЛЬ ДЕТАЛИ
# =========================
def wizard_zero():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎯 Центр"),
                KeyboardButton(text="↖ ЛВ"),
                KeyboardButton(text="↗ ПВ")
            ],
            [
                KeyboardButton(text="↙ ЛН"),
                KeyboardButton(text="↘ ПН")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# STEP 3 -- ТИП УГЛОВ (ВНУТРИ КОНТУРА)
# =========================
def wizard_corner_type():
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
# STEP 4 -- ВЫБОР УГЛОВ
# =========================
def wizard_corner_scope():
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
# STEP 5 -- ПАРАМЕТРЫ
# =========================
def wizard_params():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📏 Припуск"),
                KeyboardButton(text="🔧 Инструмент")
            ],
            [
                KeyboardButton(text="📐 Значение R/Фаски"),
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