import unittest

from services.cam_engine.simple_contour import (
    build_contour_program,
    depth_levels,
    rectangle_origin,
)


class ContourTests(unittest.TestCase):
    def test_top_zero_depths(self):
        self.assertEqual(depth_levels(5, 2, "TOP"), [-2, -4, -5])

    def test_bottom_zero_depths(self):
        self.assertEqual(depth_levels(5, 2, "BOTTOM"), [3, 1, 0])

    def test_xy_origins(self):
        self.assertEqual(rectangle_origin(40, 20, "CENTER"), (-20, -10))
        self.assertEqual(rectangle_origin(40, 20, "TR"), (-40, -20))

    def test_build_program_uses_rough_allowance_and_safe_retract(self):
        data = {
            "x": 40, "y": 20, "z": 5, "tool": 2, "tool_d": 6,
            "zero": "CENTER", "zero_z": "TOP", "rpm": 1500,
            "feed": 120, "step_z": 2, "allowance": 0.2,
            "corner": "SHARP", "corner_r": 0,
        }
        program = build_contour_program(data)
        self.assertIn("G43 H2 Z100.000", program)
        self.assertIn("G00 Z5.000", program)
        self.assertIn("G91 G28 Z0.", program)
        self.assertGreater(program.count("G03"), 0)
        self.assertGreater(program.count("G00 Z5.000"), 3)

    def test_invalid_spindle_is_rejected(self):
        data = {
            "x": 40, "y": 20, "z": 5, "tool": 2, "tool_d": 6,
            "zero": "CENTER", "zero_z": "TOP", "rpm": 16000,
            "feed": 120, "step_z": 2,
        }
        with self.assertRaises(ValueError):
            build_contour_program(data)


if __name__ == "__main__":
    unittest.main()
