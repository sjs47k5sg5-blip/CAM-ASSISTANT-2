import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db

from handlers import register_handlers


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

register_handlers(dp)


async def main():
    init_db()

    logging.info("CNC Assistant Pro started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())