import unittest

from services.cam_engine.geometry_offset import flatten_geometry, offset_geometry


def square():
    return {
        "units": "mm",
        "closed": True,
        "segments": [
            {"type": "line", "start": (0, 0), "end": (40, 0)},
            {"type": "line", "start": (40, 0), "end": (40, 20)},
            {"type": "line", "start": (40, 20), "end": (0, 20)},
            {"type": "line", "start": (0, 20), "end": (0, 0)},
        ],
    }


class GeometryOffsetTests(unittest.TestCase):
    def test_flatten_closed_square(self):
        points = flatten_geometry(square())
        self.assertEqual(len(points), 4)

    def test_outside_offset_expands_bounds(self):
        result = offset_geometry(square(), 3, "OUTSIDE")
        xs = [p[0] for s in result["segments"] for p in (s["start"], s["end"])]
        ys = [p[1] for s in result["segments"] for p in (s["start"], s["end"])]
        self.assertLessEqual(min(xs), -2.9)
        self.assertGreaterEqual(max(xs), 42.9)
        self.assertLessEqual(min(ys), -2.9)
        self.assertGreaterEqual(max(ys), 22.9)
        self.assertEqual(result["source"], "cutter_offset_preview")

    def test_inside_offset_shrinks_bounds(self):
        result = offset_geometry(square(), 3, "INSIDE")
        xs = [p[0] for s in result["segments"] for p in (s["start"], s["end"])]
        ys = [p[1] for s in result["segments"] for p in (s["start"], s["end"])]
        self.assertGreaterEqual(min(xs), 2.9)
        self.assertLessEqual(max(xs), 37.1)
        self.assertGreaterEqual(min(ys), 2.9)
        self.assertLessEqual(max(ys), 17.1)

    def test_inside_offset_rejects_collapsed_shape(self):
        with self.assertRaises(ValueError):
            offset_geometry(square(), 11, "INSIDE")

    def test_open_contour_is_rejected(self):
        geometry = square()
        geometry["closed"] = False
        with self.assertRaises(ValueError):
            offset_geometry(geometry, 2, "OUTSIDE")


if __name__ == "__main__":
    unittest.main()
