from aiogram import Dispatcher

from .back import router as back_router
from .start import router as start_router

from .face import router as face_router

from .drilling import router as drilling_router
from .threading import router as threading_router
from .milling_router import router as milling_router

from .project import router as project_router
from .reference import router as reference_router


def register_handlers(dp: Dispatcher):
    dp.include_router(back_router)
    dp.include_router(start_router)

    dp.include_router(project_router)

    dp.include_router(milling_router)
    dp.include_router(face_router)
    dp.include_router(contour_router)

    dp.include_router(drilling_router)
    dp.include_router(threading_router)

    dp.include_router(reference_router)