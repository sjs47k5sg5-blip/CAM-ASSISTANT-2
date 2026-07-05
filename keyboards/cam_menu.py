from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# =========================
# MAIN CAM MENU
# =========================
cam_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📐 Контур"), KeyboardButton(text="🟦 Карман")],
        [KeyboardButton(text="⚙️ Утилиты"), KeyboardButton(text="📚 Справочник")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите операцию CAM"
)