
from aiogram import Dispatcher

from .start import router as start_router
from .menu import router as menu_router
from .cam_router import router as cam_router

def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(cam_router)
