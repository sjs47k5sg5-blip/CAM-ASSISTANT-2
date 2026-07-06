from aiogram import Router

from .menu import router as menu_router
from .cam_flow import router as cam_router

router = Router()

router.include_router(menu_router)
router.include_router(cam_router)

def register_handlers(dp):
    dp.include_router(router)