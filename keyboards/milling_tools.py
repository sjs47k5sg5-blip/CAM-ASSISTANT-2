from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

milling_tools_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Твердосплавная"),
        ],
        [
            KeyboardButton(text="HSS"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите тип фрезы..."
)