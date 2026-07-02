from aiogram import Dispatcher

from .start import router as start_router
from .milling import router as milling_router
from .drilling import router as drilling_router


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(milling_router)
    dp.include_router(drilling_router)