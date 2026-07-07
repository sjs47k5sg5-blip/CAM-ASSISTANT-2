import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import register_handlers

TOKEN = "8914558691:AAH79JQcoHLr7qEN8uC49cKqD3LYPbNrxXQ"


async def main():

    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    register_handlers(dp)

    print("✅ CAM Assistant V5 запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())