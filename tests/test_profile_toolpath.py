import unittest

from services.cam_engine.profile_toolpath import build_profile_toolpath


def rectangle():
    return {
        "units": "mm", "closed": True,
        "segments": [
            {"type": "line", "start": (0, 0), "end": (40, 0)},
            {"type": "line", "start": (40, 0), "end": (40, 20)},
            {"type": "line", "start": (40, 20), "end": (0, 20)},
            {"type": "line", "start": (0, 20), "end": (0, 0)},
        ],
    }


class ProfileToolpathTests(unittest.TestCase):
    def test_outside_profile_has_depth_levels(self):
        result = build_profile_toolpath(rectangle(), 6, 5, 2, "OUTSIDE")
        self.assertEqual(result["z_levels"], [-2.0, -4.0, -5.0])
        self.assertGreater(result["path_count"], 0)
        self.assertEqual(result["status"], "GEOMETRY_ONLY_NOT_NC")

    def test_inside_offset_collapse_is_rejected(self):
        with self.assertRaises(ValueError):
            build_profile_toolpath(rectangle(), 30, 5, 2, "INSIDE")

    def test_invalid_stepdown_is_rejected(self):
        with self.assertRaises(ValueError):
            build_profile_toolpath(rectangle(), 6, 5, 0, "OUTSIDE")

    def test_open_contour_is_rejected(self):
        geometry = rectangle()
        geometry["closed"] = False
        with self.assertRaises(ValueError):
            build_profile_toolpath(geometry, 6, 5, 2, "OUTSIDE")


if __name__ == "__main__":
    unittest.main()
