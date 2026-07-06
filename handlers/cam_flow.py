from services.cam_engine import contour


@router.message(F.text == "ГЕНЕРАЦИЯ")
async def generate(message: Message):

    u = state(message.from_user.id)

    gcode = contour(
        x=u.size_x,
        y=u.size_y,
        depth=u.size_z,
        stepdown=u.stepdown,
        tool=u.tool,
        zero=u.zero,
        allowance=0.2,
        step=0,
        corner_type=u.mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")