def generate_gcode(x, y, depth, tool, mode):

    if mode == "pocket":
        path = f"""
(POCKET MODE)
G1 X{x} Y{y}
G1 Z-{depth}
G1 X0 Y0
"""
    else:
        path = f"""
(CONTOUR MODE)
G1 X{x} Y0
G1 X{x} Y{y}
G1 X0 Y{y}
G1 X0 Y0
"""

    return f"""
%
O1001
G21
G90
T{tool}
M6

G0 Z5

{path}

G0 Z5
M30
%
"""
