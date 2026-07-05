from aiogram import Dispatcher

from .menu import router as menu_router
from .cam import router as cam_router


# =========================
# REGISTER ALL ROUTERS
# =========================
def register_handlers(dp: Dispatcher):
    dp.include_router(menu_router)
    dp.include_router(cam_router)