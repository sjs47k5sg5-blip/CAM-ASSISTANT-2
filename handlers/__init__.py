from aiogram import Dispatcher

from .cam_router import router as cam_router
from .drilling import router as drilling_router
from .face import router as face_router
from .milling import router as milling_router
from .threading import router as threading_router
from .menu import router as menu_router
from .start import router as start_router
from .back import router as back_router


def register_handlers(dp: Dispatcher):

    # =========================
    # CAM CORE ROUTER (MAIN)
    # =========================
    dp.include_router(cam_router)

    # =========================
    # MODULE ROUTERS
    # =========================
    dp.include_router(drilling_router)
    dp.include_router(face_router)
    dp.include_router(milling_router)
    dp.include_router(threading_router)

    # =========================
    # UI ROUTERS
    # =========================
    dp.include_router(menu_router)
    dp.include_router(start_router)
    dp.include_router(back_router)