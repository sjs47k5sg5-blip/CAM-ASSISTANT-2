
def contour_gcode(width,height,depth_step,final_depth,thickness,zero_mode="top",cam_plan=None):

    lines=[]
    lines.append("%")
    lines.append("O1001")
    lines.append("G21 G90 G17")
    lines.append("G40 G49 G80")
    lines.append("G54")

    zsafe=5
    lines.append(f"G00 Z{zsafe}")

    if zero_mode=="top":
        z0=0
        d=-1
    else:
        z0=-thickness
        d=1

    depth=0
    while depth<final_depth:
        depth+=depth_step
        if depth>final_depth:
            depth=final_depth

        z=z0+depth*d

        lines.append(f"G00 Z{zsafe}")
        lines.append(f"G01 Z{z} F200")

        lines.append(f"G01 X0 Y0")
        lines.append(f"G01 X{width}")
        lines.append(f"G01 Y{height}")
        lines.append(f"G01 X0")
        lines.append(f"G01 Y0")

    lines.append("M30")
    lines.append("%")

    return "
".join(lines)
