import asyncio
from aiogram import Bot, Dispatcher

from handlers import register_handlers

TOKEN = "8914558691:AAH79JQcoHLr7qEN8uC49cKqD3LYPbNrxXQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())