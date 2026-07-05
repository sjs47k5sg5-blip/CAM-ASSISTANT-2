def contour(x,y,z,zero,allowance=0):
    safe=5
    z0=0 if zero=="top" else -z
    lines=["%","O1001 FULL CAM","G21 G90 G17","G54"]
    lines.append(f"G00 Z{safe}")

    d=0
    step=2

    while d<z:
        d+=step
        if d>z:d=z

        zz=z0-d if zero=="top" else z0+d

        lines.append(f"G00 Z{safe}")
        lines.append(f"G01 Z{zz}")
        lines.append(f"G01 X0 Y0")
        lines.append(f"G01 X{x}")
        lines.append(f"G01 Y{y}")
        lines.append(f"G01 X0 Y0")

    lines.append("M30")
    return "\n".join(lines)
