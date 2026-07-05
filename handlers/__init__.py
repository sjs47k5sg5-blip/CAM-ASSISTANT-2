from aiogram import Router

from .cam_flow import router as cam_router

router = Router()

# 🔥 подключаем ТОЛЬКО новый CAM flow
router.include_router(cam_router)


def register_handlers(dp):
    dp.include_router(router)