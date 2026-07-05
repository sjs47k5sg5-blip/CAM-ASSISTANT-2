from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# =========================
# ГЛАВНОЕ МЕНЮ
# =========================
cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Контур"), KeyboardButton(text="🟦 Карман")],
        [KeyboardButton(text="📚 Справочник"), KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)


# =========================
# ВЫБОР НУЛЯ ДЕТАЛИ
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
# ДА / НЕТ
# =========================
def yes_no_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ДА"), KeyboardButton(text="НЕТ")]
        ],
        resize_keyboard=True
    )


# =========================
# УГЛЫ ОБРАБОТКИ
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
# ЗОНЫ УГЛОВ
# =========================
def corner_zone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ВСЕ")],
            [KeyboardButton(text="ЛВ"), KeyboardButton(text="ПВ")],
            [KeyboardButton(text="ЛН"), KeyboardButton(text="ПН")]
        ],
        resize_keyboard=True
    )