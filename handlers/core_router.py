from aiogram import Router, F
from aiogram.types import CallbackQuery
from cam.engine import cam_engine

router = Router()


@router.callback_query(F.data.startswith("cam_"))
async def cam_router(callback: CallbackQuery):

    module_name = callback.data.replace("cam_", "")

    result = await cam_engine.run(
        module_name,
        {
            "user_id": callback.from_user.id
        }
    )

    await callback.message.answer(result)