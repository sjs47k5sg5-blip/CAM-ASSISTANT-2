from .router import router

from . import handlers
from . import generate

router.include_router(handlers.router)
router.include_router(generate.router)