from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def contour_menu():

    return InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📏 Размер детали",
                    callback_data="size"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🧱 Материал",
                    callback_data="material"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📍 Ноль детали",
                    callback_data="zero"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📍 Ноль Z",
                    callback_data="zero_z"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚙ Обработка углов",
                    callback_data="corner"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📉 Припуск",
                    callback_data="allowance"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔧 Инструмент",
                    callback_data="tool"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data="ready"
                )
            ]

        ]

    )