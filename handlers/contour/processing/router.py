from aiogram import Router

from .wizard import router as wizard_router
from .number_input import router as number_input_router

router = Router()

router.include_router(wizard_router)
router.include_router(number_input_router)