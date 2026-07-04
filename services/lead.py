def lead_in(
    x: float,
    y: float,
    radius: float = 5.0,
    outside: bool = True,
    climb: bool = True,
):

    if outside:

        if climb:
            arc = "G03"
        else:
            arc = "G02"

        start_x = x - radius
        start_y = y

    else:

        if climb:
            arc = "G02"
        else:
            arc = "G03"

        start_x = x + radius
        start_y = y

    return [
        f"G01 X{start_x:.3f} Y{start_y:.3f}",
        f"{arc} X{x:.3f} Y{y:.3f} R{radius:.3f}",
    ]


def lead_out(
    x: float,
    y: float,
    radius: float = 5.0,
    outside: bool = True,
    climb: bool = True,
):

    if outside:

        if climb:
            arc = "G03"
        else:
            arc = "G02"

        end_x = x - radius
        end_y = y

    else:

        if climb:
            arc = "G02"
        else:
            arc = "G03"

        end_x = x + radius
        end_y = y

    return [
        f"{arc} X{end_x:.3f} Y{end_y:.3f} R{radius:.3f}",
        "G40",
    ]