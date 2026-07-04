from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

corner_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬜ Без обработки")],
        [
            KeyboardButton(text="⭕ Радиусы"),
            KeyboardButton(text="🔷 Фаски"),
        ],
    ],
    resize_keyboard=True,
)