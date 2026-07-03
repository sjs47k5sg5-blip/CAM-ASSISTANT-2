def get_compensation(
    outside: bool,
    climb: bool,
) -> str:
    """
    Возвращает G41 или G42
    в зависимости от типа контура
    и направления фрезерования.
    """

    if outside:

        if climb:
            return "G41"

        return "G42"

    else:

        if climb:
            return "G42"

        return "G41"