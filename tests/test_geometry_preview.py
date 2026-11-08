import unittest

from services.cam_engine.geometry_preview import render_geometry_preview
from services.cam_engine.project_geometry import parse_manual_path


class GeometryPreviewTests(unittest.TestCase):
    def test_preview_is_png(self):
        geometry = parse_manual_path("M 0 0\nL 40 0\nL 40 20\nZ")
        image = render_geometry_preview(geometry)
        self.assertTrue(image.startswith(bytes([137]) + b"PNG\\r\n\\x1a\n"))


if __name__ == "__main__":
    unittest.main()
