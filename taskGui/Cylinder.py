import math

class Cylinder:
    def __init__(self, radius, height):  # Konstruktor
        self.radius = radius
        self.height = height

    def volume(self):  # Ruumala: V = πr²h
        return math.pi * self.radius ** 2 * self.height

    def baseArea(self):  # Põhjapindala: Aₚ = πr²
        return math.pi * self.radius ** 2

    def lateralSurfaceArea(self):  # Külje pindala: Aₖ = 2πrh
        return 2 * math.pi * self.radius * self.height

    def totalSurfaceArea(self):  # Kogu pindala: A = 2Aₚ + Aₖ
        return 2 * self.baseArea() + self.lateralSurfaceArea()

    def __str__(self):  # Lõppu string
        return (f"Raadius: {self.radius}\nKõrgus: {self.height}\n"
                f"Ruumala: {self.volume()}\nPõhjapindala: {self.baseArea()}\n"
                f"Külje pindala: {self.lateralSurfaceArea()}\n"
                f"Kogu pindala: {self.totalSurfaceArea()}")

