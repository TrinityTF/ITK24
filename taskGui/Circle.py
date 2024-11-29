import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
        #print(radius)

    def diameter(self):
        return self.radius * 2

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return 2 * math.pi * self.radius

    def __str__(self):
        return (f"Raadius: {self.radius}\nDiameetr: {self.diameter()}\n"
                f"Pindala: {self.area()}\nÜmbermõõt {self.circumference()}")