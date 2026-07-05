from services.entities import (
    Line,
    Arc,
)


class PathPlanner:
    """
    Планировщик траектории.

    Сначала собирает геометрию,
    затем она преобразуется в G-код.
    """

    def __init__(self):
        self.entities = []

    def clear(self):
        self.entities.clear()

    def add_line(
        self,
        start,
        end,
    ):
        self.entities.append(
            Line(
                start=start,
                end=end,
            )
        )

    def add_arc(
        self,
        start,
        end,
        center,
        clockwise,
    ):
        self.entities.append(
            Arc(
                start=start,
                end=end,
                center=center,
                clockwise=clockwise,
            )
        )

    def add_polyline(
        self,
        points,
    ):
        """
        Добавляет последовательность линий.
        """

        if len(points) < 2:
            return

        for i in range(len(points) - 1):

            self.add_line(
                points[i],
                points[i + 1],
            )

    def close_path(self):
        """
        Замыкает контур.
        """

        if len(self.entities) == 0:
            return

        first = self.entities[0]
        last = self.entities[-1]

        start = None
        end = None

        if isinstance(first, Line):
            start = first.start
        else:
            start = first.start

        if isinstance(last, Line):
            end = last.end
        else:
            end = last.end

        if start != end:

            self.add_line(
                end,
                start,
            )

    def reverse(self):
        """
        Разворачивает направление траектории.
        """

        result = []

        for entity in reversed(self.entities):

            if isinstance(entity, Line):

                result.append(
                    Line(
                        start=entity.end,
                        end=entity.start,
                    )
                )

            elif isinstance(entity, Arc):

                result.append(
                    Arc(
                        start=entity.end,
                        end=entity.start,
                        center=entity.center,
                        clockwise=not entity.clockwise,
                    )
                )

        self.entities = result

    def get_entities(self):
        return self.entities

    def __iter__(self):
        return iter(self.entities)

    def __len__(self):
        return len(self.entities)