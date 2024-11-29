import math


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * self.width + 2 * self.height

    def diagonal(self):
        return math.sqrt(self.width ** 2 + self.height ** 2)

    def __repr__(self):
        return (f"Laius: {self.width}\nKõrgus: {self.height}\n"
                f"Ümbermõõt:{self.area()}\nPindala: {self.perimeter()}")
