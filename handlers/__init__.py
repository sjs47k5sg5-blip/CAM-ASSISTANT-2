from aiogram import Dispatcher

from .menu import router as menu_router
from .milling import router as milling_router

# Контур
from .contour import router as contour_router
from .contour_size import router as contour_size_router
from .contour_material import router as contour_material_router
from .contour_zero import router as contour_zero_router
from .contour_zero_z import router as contour_zero_z_router
from .contour_corner import router as contour_corner_router
from .contour_corner_select import router as contour_corner_select_router
from .contour_corner_value import router as contour_corner_value_router
from .contour_allowance import router as contour_allowance_router
from .contour_tool import router as contour_tool_router
from .contour_generate import router as contour_generate_router


def register_handlers(dp: Dispatcher):

    # Главное меню
    dp.include_router(menu_router)

    # Фрезерная обработка
    dp.include_router(milling_router)

    # Контур
    dp.include_router(contour_router)
    dp.include_router(contour_size_router)
    dp.include_router(contour_material_router)
    dp.include_router(contour_zero_router)
    dp.include_router(contour_zero_z_router)
    dp.include_router(contour_corner_router)
    dp.include_router(contour_corner_select_router)
    dp.include_router(contour_corner_value_router)
    dp.include_router(contour_allowance_router)
    dp.include_router(contour_tool_router)
    dp.include_router(contour_generate_router)