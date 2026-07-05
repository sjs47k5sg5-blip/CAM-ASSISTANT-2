from services.contour_gcode import contour_gcode

async def contour_module(data):

    gcode = contour_gcode(
        width=20,
        height=20,
        zero_mode="top",
        thickness=20
    )

    return gcode