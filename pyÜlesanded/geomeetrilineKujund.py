import random
from math import pi

# Kujund: Silinder, ruumala valem V = pi * r^2 * h
# r - raadius
# h - kõrgus

r = float(input("Sisesta silindri raadius: ")) 
#print(f"Raadius: {r}") # Raadius

#h = float(f"{random.uniform(0, 10):.3f}") # Ümardamine
#print(f"Kõrgus: {h}") # Kõrgus

h = int(random.uniform(0, 10) * 1000) / 1000 # Arvutamine
#print(f"Kõrgus: {h}") # Kõrgus

v = pi * r**2 * h 
#print(f"Ruumala on: {v}") # Ruumala

print(f"Kujundi silinder raadiusega {r} ja kõrgusega {h} on ruumala {v}")
