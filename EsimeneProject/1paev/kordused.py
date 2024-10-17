from logging import debug
from random import randint # import RNG

names = ["Mari", "Anna", "Villem", "Jüri"]

for name in names:
    vanus = randint(1, 122)
    print(name)

print("------")
for x in range(len(names)):
    print((x+1), names[x])

print("------")
for x in range(10): # 0 - 9
    print(x)

print("------")
for x in range(1,5): # 1 - 4
    print(x)

print("------")
for x in range(0,10,2): print(x) # iga 2 [paaris arvud]tagant, 0 - 8

print("------")

# While loop

y = 0
while y < 10:
    print(y)
    y += 1 # y = y + 1

print("------")

# Ülesanne
"""Väljasta  listi names nimed lisades iga nime ette järjekorra numbri koos punktiga"""
# 1. Mari
# 2. Kadri
"""Täiendus: Tee igale nimele juhuslik vanus, kuid kirjuta kõik vanused listi nimega ages, Näita tulemus samas for loopis."""

ages = []
for x in range(len(names)):
    ages.append(randint(1, 122))
    print(f"{x+1}. {names[x]}, {ages[x]}a vana")

print(f"Ages list: {ages}")
print(f"Names list: {names}")

