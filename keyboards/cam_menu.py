from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# MAIN MENU
# =========================
cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Контур"), KeyboardButton(text="🟦 Карман")],
        [KeyboardButton(text="📚 Справочник"), KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)


# =========================
# ZERO
# =========================
def zero_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Центр детали")],
            [KeyboardButton(text="📍 ЛВ угол"), KeyboardButton(text="📍 ПВ угол")],
            [KeyboardButton(text="📍 ЛН угол"), KeyboardButton(text="📍 ПН угол")]
        ],
        resize_keyboard=True
    )


# =========================
# CORNER
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
# ALLOWANCE (NEW BUTTON SYSTEM)
# =========================
def allowance_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="0 mm")],
            [KeyboardButton(text="0.1 mm"), KeyboardButton(text="0.2 mm")],
            [KeyboardButton(text="0.5 mm"), KeyboardButton(text="1.0 mm")]
        ],
        resize_keyboard=True
    )