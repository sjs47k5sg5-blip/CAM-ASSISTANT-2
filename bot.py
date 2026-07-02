import asyncio
from aiogram import Bot,Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers.start import router
from handlers.milling import router as milling_router
bot=Bot(BOT_TOKEN)
dp=Dispatcher();dp.include_router(router)
dp.include_router(milling_router)
async def main():
 init_db();
 await dp.start_polling(bot)
if __name__=='__main__': asyncio.run(main())
