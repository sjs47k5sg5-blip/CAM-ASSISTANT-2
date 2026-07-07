from dataclasses import dataclass
import math


# ==========================================
# POINT
# ==========================================

@dataclass
class Point:

    x: float
    y: float


# ==========================================
# ARC POINT
# ==========================================

@dataclass
class ArcPoint(Point):

    i: float
    j: float

    clockwise: bool = True

    radius: float = 0


# ==========================================
# ZERO OFFSET
# ==========================================

def apply_zero(width, height, zero):

    if zero == "CENTER":
        return -width / 2, -height / 2

    if zero == "TL":
        return 0, -height

    if zero == "TR":
        return -width, -height

    if zero == "BL":
        return 0, 0

    if zero == "BR":
        return -width, 0

    return 0, 0


# ==========================================
# SHARP RECTANGLE
# ==========================================

def rectangle(width, height, tool, zero):

    ox, oy = apply_zero(width, height, zero)

    return [

        Point(ox, oy),

        Point(ox + width, oy),

        Point(ox + width, oy + height),

        Point(ox, oy + height),

        Point(ox, oy)

    ]


# ==========================================
# CHAMFER RECTANGLE
# ==========================================

def chamfer_rectangle(
        width,
        height,
        chamfer,
        tool,
        zero,
        position="ALL"
):

    ox, oy = apply_zero(width, height, zero)

    c = min(chamfer, width / 2, height / 2)

    pts = [

        Point(ox + c, oy),

        Point(ox + width - c, oy),

        Point(ox + width, oy + c),

        Point(ox + width, oy + height - c),

        Point(ox + width - c, oy + height),

        Point(ox + c, oy + height),

        Point(ox, oy + height - c),

        Point(ox, oy + c),

        Point(ox + c, oy)

    ]

    return pts


# ==========================================
# RADIUS RECTANGLE
# ==========================================

def radius_rectangle(
        width,
        height,
        radius,
        tool,
        zero,
        position="ALL"
):

    ox, oy = apply_zero(width, height, zero)

    r = min(radius, width / 2, height / 2)

    pts = [

        Point(ox + r, oy),

        Point(ox + width - r, oy),

        ArcPoint(

            ox + width,
            oy + r,

            0,
            r,

            True,
            r

        ),

        Point(ox + width, oy + height - r),

        ArcPoint(

            ox + width - r,
            oy + height,

            -r,
            0,

            True,
            r

        ),

        Point(ox + r, oy + height),

        ArcPoint(

            ox,
            oy + height - r,

            0,
            -r,

            True,
            r

        ),

        Point(ox, oy + r),

        ArcPoint(

            ox + r,
            oy,

            r,
            0,

            True,
            r

        )

    ]

    return pts


# ==========================================
# OFFSET
# ==========================================

def offset(value, tool):

    return value - tool


# ==========================================
# DISTANCE
# ==========================================

def distance(a, b):

    return math.hypot(

        b.x - a.x,

        b.y - a.y

    )


# ==========================================
# ANGLE
# ==========================================

def angle(a, b):

    return math.degrees(

        math.atan2(

            b.y - a.y,

            b.x - a.x

        )

    )