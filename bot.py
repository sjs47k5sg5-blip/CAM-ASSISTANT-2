import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers

TOKEN = "PUT_TOKEN_HERE"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
