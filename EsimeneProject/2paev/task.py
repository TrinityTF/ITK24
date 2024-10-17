"""
Ülessane:
Kirjutage skripti ring sisu nii ümber et pindala ja ümbermõõtu arvutamisks kasutatakse funksioone.
Funktsioonide nimed on
                Area()
                Perimeter()
"""
import math


def area(radius):
    ringC = 2 * math.pi * radius  # Ümbermõõt
    return ringC

def perimeter(radius):
    ringS = math.pi * radius ** 2  # Pindala
    return ringS

ringD = float(input("Ringi diameeter: min 1, max 10)....")) # Diameeter
if 1 < ringD <= 10:
    ringR = ringD / 2 # Radius
    print(f"Diameeter: {ringD}, Raadius: {ringR}, Ümbermõõt: {area(ringR)}, Pindala: {perimeter(ringR)}")

else:
    print("Vale diameeter")