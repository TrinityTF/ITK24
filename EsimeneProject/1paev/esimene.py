

name = "agu toomas pihelgas"
age = 22
height = 1.75 # Pikkus
""" Pikk Comment"""
# Lühike Comment

print(name, age, height) #Output

print(name.title() + " vanusega " + str(age) + " aastat on " + str(height) + "m pikk.") #Basic
print(f'{name.title()} vanusega {age} aastat on {height}m pikk.') #Advanced

birthYear = 2024 - age
print("Sünniaasta", birthYear)

# Vanuse kontroll
if birthYear < 1 or age > 122 :
    print("Vale aasta")
elif age < 17 :
    print("Alaealine")
elif age < 62 :
    print("Tööealine")
elif age < 100 :
    print("Pensjonär")
else :
    print("Pikaealine")
print("Scripti lõpp")

place = input("Elukoht: ")
print(f"Elukoht: {place.title()}")

"""ÜLESANNE"""
#kui sisestatud elukoht on vähem kui  7märki siis one tegemist äikse kohaga, muidu on suure kohaga

if 7 > len(place) > 1:
    print("Väike koht")
elif len(place) >= 7 :
    print("Suur koht")
elif len(place) < 2 :
    print(f"{place} on liiga lühike nimi")
else :
    print("Keskmine koht")



print("Scripti lõpp")
