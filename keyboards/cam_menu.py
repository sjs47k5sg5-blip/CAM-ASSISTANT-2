from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# ZERO SELECTION
# =========================
def zero_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Центр детали")],
            [KeyboardButton(text="📍 ЛВ угол"), KeyboardButton(text="📍 ПВ угол")],
            [KeyboardButton(text="📍 ЛН угол"), KeyboardButton(text="📍 ПН угол")],
        ],
        resize_keyboard=True
    )


# =========================
# ALLOWANCE (FINISH STOCK)
# =========================
def allowance_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="0 mm"), KeyboardButton(text="0.1 mm")],
            [KeyboardButton(text="0.2 mm"), KeyboardButton(text="0.5 mm")],
            [KeyboardButton(text="1.0 mm"), KeyboardButton(text="Без припуска")]
        ],
        resize_keyboard=True
    )


# =========================
# CORNER TYPE (FAS/ARC)
# =========================
def corner_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ФАСКА"), KeyboardButton(text="РАДИУС")],
            [KeyboardButton(text="ОСТРЫЕ")]
        ],
        resize_keyboard=True
    )


# =========================
# CORNER SELECT (WHICH CORNERS)
# =========================
def corner_select_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Все")],
            [KeyboardButton(text="ЛВ"), KeyboardButton(text="ПВ")],
            [KeyboardButton(text="ЛН"), KeyboardButton(text="ПН")],
        ],
        resize_keyboard=True
    )