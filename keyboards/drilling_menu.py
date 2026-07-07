from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def drilling_menu():

    return ReplyKeyboardMarkup(

        keyboard=[

            [
                KeyboardButton(text="🕳 Сверление")
            ],

            [
                KeyboardButton(text="🧵 Резьба")
            ],

            [
                KeyboardButton(text="🔩 Зенковка")
            ],

            [
                KeyboardButton(text="🌀 Развертка")
            ],

            [
                KeyboardButton(text="⬅ Назад")
            ]

        ],

        resize_keyboard=True

    )