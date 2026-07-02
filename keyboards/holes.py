from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

holes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🕳 Сверление"),
            KeyboardButton(text="🔩 Нарезание резьбы"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите операцию..."
)