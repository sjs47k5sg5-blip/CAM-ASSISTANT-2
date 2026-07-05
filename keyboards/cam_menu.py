from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def zero_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Центр детали")],
            [KeyboardButton(text="📍 ЛВ угол"), KeyboardButton(text="📍 ПВ угол")],
            [KeyboardButton(text="📍 ЛН угол"), KeyboardButton(text="📍 ПН угол")]
        ],
        resize_keyboard=True
    )

cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Контур"), KeyboardButton(text="🟦 Карман")],
        [KeyboardButton(text="📚 Справочник"), KeyboardButton(text="⚙️ Утилиты")]
    ],
    resize_keyboard=True
)
