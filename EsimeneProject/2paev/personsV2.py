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



src = "Persons.csv"  # Alg fail
dst = "PersonsAccountsV2.csv" # Uus fail
newHeader = ["Kasutajanimi","Epost"] # Päise kaks elementi
domains = ["@naised.org", "@mehed.org"] # Domainid

def stripAccents(s):
   # https://stackoverflow.com/questions/517923/
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
#print(stripAccents("õun Ämblik Mõõk ÄÕ ÕÜ ÜÖ ÖÄ"))

# Dünaamiline päis

oldHeaderParts = open(src, "r", encoding="utf-8").readline().strip().split(";")[:4]
header = ";".join(oldHeaderParts + newHeader)
print(header)

f = open(src,"r", encoding="utf-8") # Faili lugemine
d = open(dst, "w", encoding="utf-8") # Faili kirjutamine
contents = f.readlines() [1:] # Faili mällu lugemine teisest reast
d.write(header + "\n") # Lisa päis reavahetusega uude faili

for line in contents: # Iga row contentsis
    row = line.strip().split(";")
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
    else:
        email = username + domains[1]

    # Uue rea tegemine
    newLine = ";".join(row[:4] + [username, email])
    d.write(newLine + "\n") # Kirjuta uus rida fail koos reavahetusega

    #print(newLine) # Test
print("Valmis!")
f.close()
d.close()
# Sulgeme failid