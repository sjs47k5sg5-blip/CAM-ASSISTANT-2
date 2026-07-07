from aiogram import Router

from .roughing import router as roughing_router
from .step_z import router as step_z_router
from .stepover import router as stepover_router
from .direction import router as direction_router
from .allowance import router as allowance_router
from .finish import router as finish_router
from .finish_tool import router as finish_tool_router
from .corner_type import router as corner_type_router
from .corner_position import router as corner_position_router
from .corner_value import router as corner_value_router
from .done import router as done_router

router = Router()

router.include_router(roughing_router)
router.include_router(step_z_router)
router.include_router(stepover_router)
router.include_router(direction_router)
router.include_router(allowance_router)
router.include_router(finish_router)
router.include_router(finish_tool_router)
router.include_router(corner_type_router)
router.include_router(corner_position_router)
router.include_router(corner_value_router)
router.include_router(done_router)