from services.entities import (
    Line,
    Arc,
)

from services.arc import ij


class FanucPost:

    def __init__(self):
        self.lines = []

    def emit(self, text):
        self.lines.append(text)

    def line(self, entity: Line):

        self.emit(
            f"G01 "
            f"X{entity.end[0]:.3f} "
            f"Y{entity.end[1]:.3f}"
        )

    def arc(self, entity: Arc):

        i, j = ij(
            entity.start,
            entity.center,
        )

        code = "G02" if entity.clockwise else "G03"

        self.emit(
            f"{code} "
            f"X{entity.end[0]:.3f} "
            f"Y{entity.end[1]:.3f} "
            f"I{i:.3f} "
            f"J{j:.3f}"
        )

    def build(self, entities):

        self.lines.clear()

        for entity in entities:

            if isinstance(entity, Line):
                self.line(entity)

            elif isinstance(entity, Arc):
                self.arc(entity)

        return self.lines