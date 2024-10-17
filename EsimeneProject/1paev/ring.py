"""
Küsi kasutajalt ringi diameetrit, ning  arvuta raadius, ringi ümbermõõt ja ringi pindala.
Kõik vastused peavad olema muutujates.
Tulemuseks näita kogu infot, s.h, diameetrit.
Diameeter on murdarv (float).
Lubatud diameeter on vahemikus 1 - 10, vale mõõdu puhul teatab viga ja lõpetab töö.-
"""
import math


ringD = float(input("Ringi diameeter: min 1, max 10)....")) # Diameeter
if 1 < ringD <= 10:
    print("Õige diameeter")
    ringR = ringD / 2 # Radius
    print(f"Ringi raadius: {ringR}")
    ringC = 2 * math.pi * ringR # Ümbermõõt
    print(f"Ringi ümbermõõt: {ringC}")
    ringS = math.pi * ringR ** 2 #Pindala
    print(f"Ringi pindala: {ringS}")
    print(f"Ringi diameeter: {ringD}")
else   :
    print("Vale diameeter")

