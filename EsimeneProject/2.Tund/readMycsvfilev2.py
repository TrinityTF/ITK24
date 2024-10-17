# read my csv file v2
"""
Täiendus: Mitu numbrit leiti antud veerus.
"""
filename = "Create-MyCSV-v.csv"
column = 0 # esimene veerg
total = 0 # veergude summa
count = 0

f = open(filename, "r") # Ava fail
contents = f.readlines() # Loe faili sisu muutujasse contents
for line in contents:
    line = line.strip() # Eemaldab reavahetuse  /n
    parts = line.split(";") # Tükkelda rida semikoolonist
    if parts[column].isdigit(): # Kas kõik kolm märki on numbrid
        total += int(parts[column])
        count += 1

print(f"Total: {total}, Count: {count}") # Lõpp tulemus
f.close() # Sulge fail
