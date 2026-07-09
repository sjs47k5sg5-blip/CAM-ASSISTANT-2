from __future__ import annotations

class PassPlanner:
    """Calculates Z passes."""

    def build(self, total_depth: float, step_down: float):
        total_depth = abs(float(total_depth))
        step_down = max(abs(float(step_down)), 0.001)

        levels = []
        current = step_down

        while current < total_depth:
            levels.append(-round(current, 4))
            current += step_down

        levels.append(-round(total_depth, 4))
        return levels
