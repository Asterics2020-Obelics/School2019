"""Exception example.

(code is pointless, just to make a simple example)
"""
from point import Point

def move_it(point):
    point.move(42, '43')

def main():
    p = Point(1, 2)
    move_it(p)

main()
