from point import Point, distance

p1 = Point(3, 0)
p2 = Point(0, 3)
p2.move(0, 1)

d = distance(p1, p2)
print(d)
