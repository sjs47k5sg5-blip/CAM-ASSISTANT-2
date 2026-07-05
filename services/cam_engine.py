import math


class CAMEngine:

    # =========================
    # ENTRY POINT
    # =========================
    def build(self, data):

        thickness = float(data.get("thickness", 0))
        step_down = float(data.get("step", 2.0))

        return {
            "strategy": self.get_strategy(data),
            "depths": self.calc_depths(thickness, step_down),
            "finish_pass": self.finish_pass(data),
            "rough_pass": self.rough_pass(data),
            "radius": data.get("radius", False),
            "chamfer": data.get("chamfer", False),
            "stock_to_leave": 0.2
        }


    # =========================
    # STRATEGY SELECTOR
    # =========================
    def get_strategy(self, data):

        tool = data.get("tool", "endmill")
        material = data.get("material", "steel")

        if material == "aluminum":
            return "high_speed"

        if material == "steel":
            return "balanced"

        if tool == "endmill":
            return "standard"

        return "safe"


    # =========================
    # DEPTH CALCULATION
    # =========================
    def calc_depths(self, thickness, step):

        if thickness <= 0:
            return [0]

        depths = []
        current = 0

        while current < thickness:
            current += step
            if current > thickness:
                current = thickness
            depths.append(round(current, 3))

        return depths


    # =========================
    # ROUGH PASS
    # =========================
    def rough_pass(self, data):

        return {
            "enabled": True,
            "step_over": 0.6,
            "feed_factor": 1.0,
            "spindle_factor": 0.9
        }


    # =========================
    # FINISH PASS
    # =========================
    def finish_pass(self, data):

        return {
            "enabled": True,
            "step_over": 0.2,
            "feed_factor": 0.6,
            "spindle_factor": 1.0
        }


    # =========================
    # TOOLPATH HELPERS
    # =========================
    def safe_feed(self, base_feed, material):

        if material == "steel":
            return base_feed * 0.8

        if material == "aluminum":
            return base_feed * 1.2

        return base_feed


    def safe_rpm(self, diameter, material):

        base = 10000 / max(diameter, 1)

        if material == "steel":
            return int(base * 0.7)

        if material == "aluminum":
            return int(base * 1.3)

        return int(base)