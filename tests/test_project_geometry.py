import unittest
from services.cam_engine.project_geometry import parse_manual_path

class GeometryTests(unittest.TestCase):
    def test_arc_and_line(self):
        data = parse_manual_path("M 0 0\nL 20 0\nA 20 20 0 10 CCW\nZ")
        self.assertEqual(len(data["segments"]), 3)
        self.assertTrue(data["closed"])

    def test_invalid_arc(self):
        with self.assertRaises(ValueError):
            parse_manual_path("M 0 0\nA 20 20 0 5 CCW")

if __name__ == "__main__":
    unittest.main()
