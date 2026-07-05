from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Контур"), KeyboardButton(text="Карман")],
        [KeyboardButton(text="Утилиты"), KeyboardButton(text="Справочник")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)