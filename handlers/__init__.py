from aiogram import Dispatcher

from .menu import router as menu_router
from .contour.router import router as contour_router
from .pocket import router as pocket_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(contour_router)
    dp.include_router(pocket_router)
    dp.include_router(menu_router)
