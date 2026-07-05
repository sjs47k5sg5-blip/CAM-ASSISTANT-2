def generate_gcode(x, y, step, depth):
    return f"""
%
O1001
G21
G90

; X={x} Y={y}
; STEP={step}
; DEPTH={depth}

G0 Z5
G0 X0 Y0

G1 Z-{depth} F100

G1 X{x} Y0
G1 X{x} Y{y}
G1 X0 Y{y}
G1 X0 Y0

G0 Z5
M30
%
"""