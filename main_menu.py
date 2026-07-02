from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main_menu=ReplyKeyboardMarkup(
keyboard=[
[KeyboardButton(text="📐 Режимы резания"),KeyboardButton(text="📊 Калькуляторы")],
[KeyboardButton(text="⚙️ Генерация G-кода")],
[KeyboardButton(text="🛠 Инструменты"),KeyboardButton(text="📚 G/M-коды")],
[KeyboardButton(text="ℹ️ О программе")]
],resize_keyboard=True)
