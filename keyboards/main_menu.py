from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 CAM")],
        [KeyboardButton(text="📚 Справочник")]
    ],
    resize_keyboard=True
)