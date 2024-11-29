import math

class Cone:
    def __init__(self, radius, height): # Konstruktor
        self.radius = radius
        self.height = height

    def slant_height(self): # Moodustaja: s = √(r² + h²)
        return math.sqrt(self.radius ** 2 + self.height ** 2)

    def volume(self): # Ruumala: V = (1/3)πr²h
        return (1/3) * math.pi * self.radius ** 2 * self.height

    def base_area(self): # Põhjapindala: Aₚ = πr²
        return math.pi * self.radius ** 2

    def lateral_surface_area(self): # Külje pindala: Aₖ = πrs
        return math.pi * self.radius * self.slant_height()

    def total_surface_area(self): # Kogu pindala: A = Aₖ + Aₚ
        return self.lateral_surface_area() + self.base_area()

    def __str__(self): # Lõpp string
        return (f"Raadius: {self.radius}\nKõrgus: {self.height}\n"
                f"Moodustaja: {self.slant_height()}\nRuumala: {self.volume()}\n"
                f"Põhjapindala: {self.base_area()}\nKülje pindala: {self.lateral_surface_area()}\n"
                f"Kogu pindala: {self.total_surface_area()}")