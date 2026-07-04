from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_tool_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Тем же инструментом"),
        ],
        [
            KeyboardButton(text="🔄 Выбрать другой инструмент"),
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
        ],
    ],
    resize_keyboard=True,
)