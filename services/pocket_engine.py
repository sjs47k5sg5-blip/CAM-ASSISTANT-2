def pocket_gcode(w,h,depth):
 lines=["%","O2000 POCKET V8","G21 G90 G17","G54"]
 step=2
 o=0
 z=-depth
 while w-2*o>0 and h-2*o>0:
  x0,y0=o,o
  x1,y1=w-o,h-o
  lines.append(f"G01 Z{z}")
  lines.append(f"G01 X{x0} Y{y0}")
  lines.append(f"G01 X{x1} Y{y0}")
  lines.append(f"G01 X{x1} Y{x1}")
  lines.append(f"G01 X{x0} Y{x1}")
  o+=step
 lines += ["M30","%"]
 return "\n".join(lines)
