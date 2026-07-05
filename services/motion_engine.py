
class MotionEngine:
    def line(self,x,y,f=300):
        return f"G01 X{x} Y{y} F{f}"
