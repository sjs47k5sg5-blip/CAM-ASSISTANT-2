from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = []

number = 1

for _ in range(6):
    row = []

    for _ in range(5):
        row.append(
            KeyboardButton(text=f"T{number}")
        )
        number += 1

    keyboard.append(row)

keyboard.append(
    [KeyboardButton(text="⬅️ Назад")]
)

tool_number_keyboard = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True,
)