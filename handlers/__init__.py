from aiogram import Router

from .menu import router as menu_router
from .cam_flow import router as cam_router
from .milling import router as milling_router
from .holes import router as holes_router
from .manual import router as manual_router
from .about import router as about_router

router = Router()

router.include_router(menu_router)   # 🔥 ВАЖНО
router.include_router(cam_router)
router.include_router(milling_router)
router.include_router(holes_router)
router.include_router(manual_router)
router.include_router(about_router)


def register_handlers(dp):
    dp.include_router(router)