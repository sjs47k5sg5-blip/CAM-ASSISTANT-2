from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

corner_select_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="☑ Все")],
        [
            KeyboardButton(text="◤ Левый верхний"),
            KeyboardButton(text="◥ Правый верхний"),
        ],
        [
            KeyboardButton(text="◣ Левый нижний"),
            KeyboardButton(text="◢ Правый нижний"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)