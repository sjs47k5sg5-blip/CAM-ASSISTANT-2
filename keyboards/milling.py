from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

milling_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📐 Режимы резания", callback_data="cam_modes")
    ],
    [
        InlineKeyboardButton(text="🟦 Торцевое фрезерование", callback_data="cam_face")
    ],
    [
        InlineKeyboardButton(text="⭕ Контур", callback_data="cam_contour")
    ],
    [
        InlineKeyboardButton(text="⬜ Карман", callback_data="cam_pocket")
    ],
    [
        InlineKeyboardButton(text="➖ Паз", callback_data="cam_slot")
    ],
    [
        InlineKeyboardButton(text="🌀 Винтовая интерполяция", callback_data="cam_helical")
    ],
    [
        InlineKeyboardButton(text="⬅️ Назад", callback_data="cam_back")
    ]
])