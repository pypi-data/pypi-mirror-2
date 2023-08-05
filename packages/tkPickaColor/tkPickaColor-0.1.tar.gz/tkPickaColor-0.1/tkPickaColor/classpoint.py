
class Point(object):
    def __init__(self, coord=(0, 0)):
        self.x , self.y = coord

    def reset(self):
        self.x = 0
        self.y = 0

    def __add__(self, p):
        "Add 2 points, return a new point"
        return Point(self.x + p.x, self.y + p.y)

    def copy(self, other):
        "replace self's xy with another's point"
        self.x = other.x
        self.y = other.y

    def move_rel(self, deltas):
        "change current x,y by adding the deltas"
        dx, dy = deltas
        self.x += dx
        self.y += dy

    def move_abs(self, newCoord):
        self.x, self.y = newCoord

    def __repr__(self):
        "return a string representation of this point."
        return 'Point(%d,%d)' % (self.x, self.y)

if __name__ == '__main__':
    p = Point((5, 6))
    print p
    q = Point((2, 2))
    p.copy(q)
    p.move_rel((10, 10))
    print p
