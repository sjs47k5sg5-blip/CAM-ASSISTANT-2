import unittest

from services.cam_engine.pocket import (
    build_pocket_program,
    depth_levels,
    pocket_origin,
    raster_path,
)


class PocketTests(unittest.TestCase):
    def sample(self):
        return {
            "x": 100, "y": 80, "depth": 4, "tool": 4, "tool_d": 8,
            "zero": "CENTER", "zero_z": "TOP", "rpm": 1500,
            "feed": 120, "step_z": 1, "stepover": 40, "allowance": 0.2,
        }

    def test_depth_levels(self):
        self.assertEqual(depth_levels(5, 2, "TOP"), [-2, -4, -5])
        self.assertEqual(depth_levels(5, 2, "BOTTOM"), [3, 1, 0])

    def test_origins(self):
        self.assertEqual(pocket_origin(100, 80, "CENTER"), (-50, -40))
        self.assertEqual(pocket_origin(100, 80, "TR"), (-100, -80))

    def test_raster_inside_limits(self):
        points = raster_path(4, 4, 96, 76, 3)
        self.assertTrue(all(4 <= px <= 96 and 4 <= py <= 76 for px, py in points))

    def test_program_has_rough_and_finish(self):
        program = build_pocket_program(self.sample())
        self.assertIn("O1003", program)
        self.assertIn("(ROUGH POCKET PASS 4)", program)
        self.assertIn("(FINISH FLOOR)", program)
        self.assertIn("(FINISH WALL)", program)
        self.assertIn("G43 H4 Z100.000", program)
        self.assertIn("G91 G28 Z0.", program)

    def test_bottom_zero_safe_height(self):
        data = self.sample()
        data["zero_z"] = "BOTTOM"
        program = build_pocket_program(data)
        self.assertIn("G43 H4 Z104.000", program)
        self.assertIn("G00 Z9.000", program)

    def test_rejects_tool_too_large(self):
        data = self.sample()
        data["tool_d"] = 90
        with self.assertRaises(ValueError):
            build_pocket_program(data)

    def test_rejects_bad_stepover(self):
        data = self.sample()
        data["stepover"] = 90
        with self.assertRaises(ValueError):
            build_pocket_program(data)

    def test_rejects_ramp_too_steep(self):
        data = self.sample()
        data["x"], data["y"], data["step_z"] = 20, 20, 10
        with self.assertRaises(ValueError):
            build_pocket_program(data)

    def test_bottom_zero_uses_incremental_step_for_ramp(self):
        data = self.sample()
        data.update({"x": 40, "y": 30, "depth": 10, "step_z": 2, "zero_z": "BOTTOM"})
        program = build_pocket_program(data)
        self.assertIn("(ROUGH POCKET PASS 5)", program)
        self.assertIn("G43 H4 Z110.000", program)


if __name__ == "__main__":
    unittest.main()
