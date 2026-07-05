from cam.engine import cam_engine
from modules.contour import contour_module
from modules.pocket import pocket_module

def load_modules():
    cam_engine.register("contour", contour_module)
    cam_engine.register("pocket", pocket_module)