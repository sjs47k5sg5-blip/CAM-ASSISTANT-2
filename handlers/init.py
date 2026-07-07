from aiogram import Dispatcher

from .menu import router as menu_router
from .milling import router as milling_router
from .holes import router as holes_router
from .about import router as about_router
from .handbook import router as handbook_router

from .contour.router import router as contour_router


def register_handlers(dp: Dispatcher):

    dp.include_router(menu_router)
    dp.include_router(milling_router)
    dp.include_router(holes_router)
    dp.include_router(about_router)
    dp.include_router(handbook_router)

    dp.include_router(contour_router)