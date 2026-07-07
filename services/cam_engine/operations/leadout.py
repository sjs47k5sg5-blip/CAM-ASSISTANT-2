from services.cam_engine.toolpath import Rapid


def build_leadout(
    toolpath,
    safe_z,
):
    """
    Безопасный отход инструмента после прохода.
    """

    toolpath.add(

        Rapid(
            z=safe_z,
        )

    )