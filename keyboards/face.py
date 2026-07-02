from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

face_strategy_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🟦 По строкам"),
        ],
        [
            KeyboardButton(text="🌀 Зигзаг"),
        ],
        [
            KeyboardButton(text="↔️ Односторонняя"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите стратегию..."
)