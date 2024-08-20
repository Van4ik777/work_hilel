import math


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2

    def __str__(self):
        return f"Circle({self.x}, {self.y}, {self.radius})"


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height

    def __str__(self):
        return f"Rectangle({self.x}, {self.y}, {self.height}, {self.width})"


class Parallelogram(Rectangle):
    # S = a * b * sin(α)
    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}, {self.x}, {self.y}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.x * self.y * math.sin(math.radians(self.angle))


class Triangle(Shape):
    def __init__(self, x, y, base, height):
        super().__init__(x, y)
        self.base = base
        self.height = height

    def square(self):
        return self.base * self.height * 0.5

    def __str__(self):
        return f'Triangle: {self.base}, {self.height}, {self.x}, {self.y}'


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        return '\n'.join(str(i) for i in self._figures)


r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, -10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)

p = Parallelogram(1, 2, 20, 30, 45)
p.x
p1 = Parallelogram(1, 2, 20, 30, 45)
str(p1)

t = Triangle(10, 5, 10, 5)
t1 = Triangle(10, 5, 10, 12)

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)
scene.add_figure(t)
scene.add_figure(t1)
print(scene.total_square())

print(scene)

print(f'Total square of all figures: {scene.total_square()}')


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __contains__(self, point: object) -> bool:
        distance = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        return distance <= self.radius


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


circle = Circle(0, 5, 10)
point = Point(0, 15)

print(point in circle)
