from services.cam_engine.toolpath import (
    Rapid,
    Feed,
)


def build_leadin(
    toolpath,
    point,
    depth,
    safe_z,
    rapid_z,
    plunge_feed,
):

    # Подъем в безопасную высоту
    toolpath.add(
        Rapid(
            z=safe_z,
        )
    )

    # Быстрый подход по XY
    toolpath.add(
        Rapid(
            x=point.x,
            y=point.y,
        )
    )

    # Быстрый подход над деталью
    toolpath.add(
        Rapid(
            z=rapid_z,
        )
    )

    # Рабочее врезание
    toolpath.add(
        Feed(
            z=depth,
            feed=plunge_feed,
        )
    )