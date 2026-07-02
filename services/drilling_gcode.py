def drilling_g81(
    tool: int,
    rpm: int,
    feed: int,
    x: float,
    y: float,
    depth: float,
    r_plane: float,
):

    return f"""%
O2001
(DRILL G81)

G21
G17
G90
G40
G49
G80

T{tool} M06
G54

S{rpm} M03
M08

G00 G43 H01 Z50.

X{x:.3f} Y{y:.3f}

G98 G81 Z-{depth:.3f} R{r_plane:.3f} F{feed}

G80

G00 Z100.

M09
M05

M30
%
"""