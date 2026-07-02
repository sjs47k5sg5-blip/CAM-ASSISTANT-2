def threading_gcode(
    tool: int,
    rpm: int,
    feed: int,
    depth: float,
):
    return f"""%
O1001

(THREADING)

G21
G17
G90
G40
G49
G80

T{tool} M06

G54

S{rpm} M03
M29
M08

G00 G43 H01 Z50.

G00 X0. Y0.

G84 Z-{depth:.3f} R2.0 F{feed}

G80

G00 Z100.

M09
M05

M30
%
"""