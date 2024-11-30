import math

class Cone:
    def __init__(self, radius, height): # Konstruktor
        self.radius = radius
        self.height = height

    def slantHeight(self): # Moodustaja: s = √(r² + h²)
        return math.sqrt(self.radius ** 2 + self.height ** 2)

    def volume(self): # Ruumala: V = (1/3)πr²h
        return (1/3) * math.pi * self.radius ** 2 * self.height

    def baseArea(self): # Põhjapindala: Aₚ = πr²
        return math.pi * self.radius ** 2

    def lateralSurfaceArea(self): # Külje pindala: Aₖ = πrs
        return math.pi * self.radius * self.slantHeight()

    def totalSurfaceArea(self): # Kogu pindala: A = Aₖ + Aₚ
        return self.lateralSurfaceArea() + self.baseArea()

    def __str__(self): # Lõpp string
        return (f"Raadius: {self.radius}\nKõrgus: {self.height}\n"
                f"Moodustaja: {self.slantHeight()}\nRuumala: {self.volume()}\n"
                f"Põhjapindala: {self.baseArea()}\nKülje pindala: {self.lateralSurfaceArea()}\n"
                f"Kogu pindala: {self.totalSurfaceArea()}")