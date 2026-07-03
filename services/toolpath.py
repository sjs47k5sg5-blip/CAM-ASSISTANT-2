def get_compensation(
    outside: bool,
    climb: bool,
) -> str:

    if outside and climb:
        return "G41"

    if outside and not climb:
        return "G42"

    if not outside and climb:
        return "G42"

    return "G41"


def get_arc(
    outside: bool,
    climb: bool,
) -> str:

    if outside and climb:
        return "G03"

    if outside and not climb:
        return "G02"

    if not outside and climb:
        return "G02"

    return "G03"