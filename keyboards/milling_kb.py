from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

milling_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Контур", callback_data="cam_contour")],
    [InlineKeyboardButton(text="Карман", callback_data="cam_pocket")],
    [InlineKeyboardButton(text="Торец", callback_data="cam_face")],
    [InlineKeyboardButton(text="Паз", callback_data="cam_slot")],
    [InlineKeyboardButton(text="Винтовая", callback_data="cam_helical")]
])