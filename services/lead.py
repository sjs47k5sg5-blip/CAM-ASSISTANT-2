def lead_in(
    x: float,
    y: float,
    radius: float = 5.0,
):
    return [
        f"G01 X{x-radius:.3f} Y{y:.3f}",
        f"G03 X{x:.3f} Y{y:.3f} R{radius:.3f}",
    ]


def lead_out(
    x: float,
    y: float,
    radius: float = 5.0,
):
    return [
        f"G03 X{x-radius:.3f} Y{y:.3f} R{radius:.3f}",
        "G40",
    ]