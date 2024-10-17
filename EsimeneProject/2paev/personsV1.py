# read persons v1
"""
Luua igale kasutajale kasutajanimi ja epost adress.
Kasutajanimi:
    eesnimi.perekonnanimi
    eesnimes eemaldada sidekiriips ja tühik
    kasautajanimes eemaldada rõhumärgid
    kasutajanimes on läbivalt väiksed tähed
Epost Aadress:
    naistel on @naised.org
    meestel on @mehed.org
    kasutajanimi@domain

Uue faili sisu on:
    Eesnimi;Pereimi;Sünniaeg;Sugu;Kasutajanimi;Epost
_______________________________________________________________________________________
"""
import unicodedata
import csv

src = "Persons.csv"  # Alg fail
dst = "PersonsAccounts.csv"  # Uus fail
header = "Eesnimi;Pereimi;Sünniaeg;Sugu;Kasutajanimi;Epost" # Päis
domains = ["@naised.org", "@mehed.org"] # Domainid

def stripAccents(s):
   # https://stackoverflow.com/questions/517923/
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
#print(stripAccents("õun Ämblik Mõõk ÄÕ ÕÜ ÜÖ ÖÄ"))

f = open(src,"r", encoding="utf-8") # Faili lugemine
d = open(dst, "w", encoding="utf-8") # Faili kirjutamine
        contents = csv.reader(f, delimiter=";")
        headerOriginal = next(contents) # Hakkab lugema 2. reast
        d.write(header + "\n") # Lisa päis reavahetusega uude faili
        for row in contents: # Iga row contentsis

            firstName = row[0]
            lastName = row[1]

            firstName = firstName.replace(" ", "")
            firstName = firstName.replace("-", "")

            lastName = lastName.replace(" ", "")
            lastName = lastName.replace("-", "")

            # Kasutajanime loomine
            username = ".".join([firstName, lastName]).lower()
            # Eemalda rõhumärgid
            username = stripAccents(username)

            if row[3] == "N":
                email = username + domains[0]
            elif row[3] == "M":
                email = username + domains[1]
            else:
                print("Sugu vale")
            # Uue rea tegemine
            newLine = ";".join(row[:4] + [username, email])
            d.write(newLine + "\n") # Kirjuta uus rida fail koos reavahetusega

            #print(newLine) # Test
print("Valmis!")