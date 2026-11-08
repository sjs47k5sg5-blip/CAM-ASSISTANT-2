import unittest

from services.cam_engine.geometry_validation import build_rounded_polygon, validate_geometry


class RoundedGeometryTests(unittest.TestCase):
    def test_each_corner_has_its_own_radius(self):
        geometry = build_rounded_polygon([
            (0, 0, 5), (80, 0, 10), (80, 40, 2), (0, 40, 0)
        ])
        arcs = [segment for segment in geometry["segments"] if segment["type"] == "arc"]
        self.assertEqual(len(arcs), 3)
        self.assertEqual(validate_geometry(geometry), [])

    def test_rejects_radius_that_does_not_fit(self):
        with self.assertRaises(ValueError):
            build_rounded_polygon([
                (0, 0, 30), (40, 0, 30), (40, 20, 0), (0, 20, 0)
            ])

    def test_rejects_concave_polygon(self):
        with self.assertRaises(ValueError):
            build_rounded_polygon([
                (0, 0, 0), (40, 0, 0), (20, 10, 0), (0, 20, 0)
            ])


if __name__ == "__main__":
    unittest.main()
