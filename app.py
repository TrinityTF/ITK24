from random import randint

from Circle import Circle #from failinimi, import klassinimi
from Rectangle import Rectangle

circle = Circle(5)
circle2 = Circle("test")
circle3 = Circle(10)
print(circle2.radius)

# Arvuta diameeter
print(circle.diameter())
print(circle2.diameter())
print(circle3.diameter())

# Aruvta pindala
print(circle.area())
#print(circle2.area())
print(circle3.area())

# Arvuta pidala
print(circle.circumference())
#print(circle2.circumference())
print(circle3.circumference())

# Kas circle 1 on suurem/väiksem kui circle 3
if circle.radius < circle3.radius:
    print("Circle on suurem")
else:
    print("Circle on väiksem")

# Väljasta object
print(circle)

# Uus raadius
#radius = float(input("Sisesta uus radius: "))
#circle.radius = radius
#print(circle3)

# Genereeri 5 juhusliku ringi raadiust ja näita tulemusi (1-10)
for i in range(5):
    ranRadius = randint(1, 10)
    ranCircle = Circle(ranRadius)
    print(f"Juhuslik circle {i+1}: Raadius = {ranCircle.radius}, Diameeter = {ranCircle.diameter()}, Pindala = {ranCircle.area()}, Ümbermõõt = {ranCircle.circumference()}")


#Vahe
print("________________________________________________________________________________________________________________________________")

#Ristkülik
ristkulik = Rectangle(10, 5)

print(f"Ristküliku andmed: "
      f"Pindala: {ristkulik.area()}, "
      f"Ümbermõõt: {ristkulik.perimeter()}, "
      f"Diagonaal: {ristkulik.diagonal()} ")
