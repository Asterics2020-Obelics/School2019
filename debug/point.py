import math

def distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    d2 = dx * dx + dy * dy
    return math.sqrt(d2)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
