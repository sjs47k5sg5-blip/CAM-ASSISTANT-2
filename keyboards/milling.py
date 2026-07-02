from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

milling_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📐 Режимы резания"),
        ],
        [
            KeyboardButton(text="🟦 Торцевое фрезерование"),
        ],
        [
            KeyboardButton(text="⭕ Контур"),
            KeyboardButton(text="⬜ Карман"),
        ],
        [
            KeyboardButton(text="📏 Паз"),
            KeyboardButton(text="🌀 Винтовая интерполяция"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите операцию..."
)