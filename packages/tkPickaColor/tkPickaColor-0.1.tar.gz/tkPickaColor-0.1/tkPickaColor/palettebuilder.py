from Tkinter import *
from colorservices import *
from classpoint import Point

class HarmonyPalettes(object):
#    START = (5, 5)
    def __init__(self, canv, rgb = "#05ff05", size = 20, spacer = 2):
        canv.config(height = 375, width = 500)
        baseRGB = rgb
        baseHSV = getHSV(baseRGB)
        harmonies = [("Base Color - Tints & Shades", (0,)),
                            ("Complementary - RGB color space", (180,)),
                            ("Split complementary - RGB", (150, 210)),
                            ("Triad - RGB", (120, 240))]
        start = (10, 20)
        square = Square(start, canv, size = size, spacer = spacer)
        origin = Square(start, canv, size = size, spacer = spacer)
        large = LargeSquare(start, canv, size = size, spacer = spacer)

        for name, angles in harmonies:
            canv.create_text(origin.x, origin.y + 4, text = name, anchor = NW)
            origin.move_next_row()
            large.copy(origin)
            xoffset = large.row1Coord()[0]
            square.move_abs((xoffset, origin.y))

            for angle in angles:
                newHSV = self.rotateHue(baseHSV, angle)
                newRGB = getRGB(newHSV)
                large.draw(newRGB)
                tints = self.getTints(newHSV, 10, 5)
                shades = self.getShades(newHSV, 10, 5)
                for tint in tints:
                    square.draw(tint)
                origin.move_next_row()
                square.move_abs((xoffset, origin.y))
                for shade in shades:
                    square.draw(shade)
                origin.move_next_row()
                large.copy(origin)
                square.move_abs((xoffset, origin.y))

    def rotateHue(self, baseHSV, angle):
        hue, sat, val = baseHSV
        sum = hue + angle
#         hue,  sum
        if sum > 360:
#            sum = sum - 360
            sum -= 360
        return ((sum, sat, val))

    def getTints(self, baseHSV, steps = 10, stepValue = 10):
        '''return array of colors that vary the saturation\
        the original color plus three tints to either side'''
        tints = []
        h, s, v = baseHSV
        for sat in range (100, 0, -5):
            tints.append(getRGB((h, sat, v)))
        return tints

    def getShades(self, baseHSV, steps = 10, stepValue = 10):
        '''return array of colors that vary the saturation\
        the original color plus three tints to either side'''
        shades = []
        h, s, val = baseHSV
        for val in range (100, 0, -5):
            shades.append(getRGB((h, s, val)))
        return shades

class DrawPalette(object): #for gimp and favorites
    "draws squares untill list is exausted"
    def __init__(self, canv, colors, name = '', columns = 16, size = 20,
                 spacer = 2, start = (5, 5), tags = False):
        if not tags:
            square = Square(start, canv, size = size, spacer = spacer)
        else:    # i.e. favorites with tags
            square = SquareWithTags(start, canv, size = size, spacer = spacer)
        origin = square.duplicate()
        rgb = (color for color in colors)
        if name:
            self.draw_text(canv, name, origin)
        self.draw_squares(canv, rgb, origin, columns)

    def draw_text(self, canv, name, origin):
        x, y = origin.x, origin.y
        canv.create_text(x, y + 3, text = name, anchor = W)
        origin.move_next_row()

    def draw_squares(self, canv, rgb, origin, columns):
        def move():
            origin.move_next_row()
            square.copy(origin)
        square = origin.duplicate()
        while True:
            for col in range(columns):
                try:
                    square.draw(rgb.next())
                except StopIteration: #out of colors
                    move()
                    return
            move()

class Square(Point): # general gimp palette builder
    def __init__(self, coord = (0, 0), canvas = None, size = 10, spacer = 1):
        Point.__init__(self, coord)
        self.size = size
        self.spacer = spacer
        self.canvas = canvas

    def duplicate(self):
        return Square((self.x, self.y), self.canvas, self.size, self.spacer)

    def move_next_col(self):
        self.x += self.size + self.spacer
        return (self.x, self.y)

    def move_next_row(self):
        self.y += self.size + self.spacer
        return (self.x, self.y)

    def corners(self):
        d = self.size
        return (self.x, self.y, self.x + d, self.y + d)

    def draw(self, color):
        self.canvas.create_rectangle(self.corners(), fill = color)
        self.move_next_col()

class SquareWithTags(Square): # working with favorites
    def __init__(self, coord = (0, 0), canvas = None, size = 10, spacer = 1):
        Square.__init__(self, coord, canvas, size, spacer)
        self.tag = ("tag" + str(n).rjust(4, "0") for n in xrange (1, 1000)) # 1000 is just any big number
    # !!!! canvas object ids appears to start @ 1
    def  duplicate(self):
        return SquareWithTags((self.x, self.y), self.canvas, self.size, self.spacer)

    def draw(self, color):
#        if color == "" : #create unfilled square
#            self.canvas.create_rectangle(self.corners(), tags = self.tag.next())
#        else:
        self.canvas.create_rectangle(self.corners(), fill = color, tags = self.tag.next())
        self.move_next_col()

class LargeSquare(Square):
    def __init__(self, coord = (0, 0), canvas = None, size = 10, spacer = 1):
        Square.__init__(self, coord, canvas, size, spacer)
        self.size = size * 2
        self.canvas = canvas

    def row1Coord(self):
        delta = self.size + self.spacer * 2
        return ((self.x + delta, self.y))

    def draw(self, color):
        d = self.size + self.spacer
        self.canvas.create_rectangle(self.x, self.y, self.x + d, self.y + d, fill = color)

if __name__ == '__main__':
    root = Tk()
    c = Canvas(root, height = 500, width = 500)
    c.pack()
    HarmonyPalettes(c, '#00FF00')
    root.mainloop()
