import math

class Triangle:
    def __init__(self, sideA, sideB):  # Konstruktor
        self.sideA = sideA
        self.sideB = sideB

    def hypotenuse(self):  # Hüpotenus: c = √(a² + b²)
        return math.sqrt(self.sideA ** 2 + self.sideB ** 2)

    def area(self):  # Pindala: A = (1/2)ab
        return 0.5 * self.sideA * self.sideB

    def perimeter(self):  # Ümbermõõt: P = a + b + c
        return self.sideA + self.sideB + self.hypotenuse()

    def __str__(self):  # Lõpp string
        return (f"Külg a: {self.sideA}, Külg b = {self.sideB}\n"
                f"Hüpotenuus: {self.hypotenuse()}\n"
                f"Pindala: {self.area()}\n"
                f"Ümbermõõt: {self.perimeter()}")