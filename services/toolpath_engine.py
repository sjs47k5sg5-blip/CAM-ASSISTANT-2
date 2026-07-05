
class ToolpathEngine:

    def contour(self, w, h, o=0):
        return [(o,o),(w-o,o),(w-o,h-o),(o,h-o),(o,o)]

    def pocket(self, w, h, step=2):
        paths=[]
        o=0
        while w-2*o>0 and h-2*o>0:
            paths.append([(o,o),(w-o,o),(w-o,h-o),(o,h-o),(o,o)])
            o+=step
        return paths
