from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

zero_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="↙️ Левый нижний"),
            KeyboardButton(text="↖️ Левый верхний"),
        ],
        [
            KeyboardButton(text="↘️ Правый нижний"),
            KeyboardButton(text="↗️ Правый верхний"),
        ],
        [
            KeyboardButton(text="⭕ Центр детали"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)