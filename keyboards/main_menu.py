from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📂 Проект"),
        ],
        [
            KeyboardButton(text="📐 Фрезерование"),
            KeyboardButton(text="🕳 Отверстия"),
        ],
        [
            KeyboardButton(text="📚 Справочник"),
            KeyboardButton(text="⚙️ Утилиты"),
        ],
        [
            KeyboardButton(text="ℹ️ О программе"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел..."
)