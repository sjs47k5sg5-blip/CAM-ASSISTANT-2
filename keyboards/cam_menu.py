from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cam_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Контур", callback_data="cam_contour")],
    [InlineKeyboardButton(text="Карман", callback_data="cam_pocket")]
])
