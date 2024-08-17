import math


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, point: object) -> bool:
        distance = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        print(distance)
        return distance <= self.radius


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

circle= Circle(0, 5, 10)
point = Point(1, 15)

print(point in circle)
