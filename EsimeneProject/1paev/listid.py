#Listid

places = [] # Tühi list
places.append("Kehtna") # Lisa juurde
places.append("Rapla")
places[1:1] = ["Tallinn", "Pärnu"] # Lisa Kehtna ja Rapla vahele
places.extend(["Viljandi", "Tartu", "Rapla"]) # Lisa lõppu
places.insert(2,"Are") # Lis kindlasse kohta

print(f"Enne kustutamist: {places}")
places.remove("Rapla") # Kustudab nime järgi esimese
places.pop(6) # Seitsmes koht [Viimane Rapla]

#Test
print(places)

# Muud tegemised listiga

placesSize = len(places)
print("Listi suurus", placesSize)

places.sort() # A - Z
places.reverse() # Z - A
print(places)