# read my csv file v1

filename = "Create-MyCSV-v.csv"
#column = 0 # esimene veerg
total = 0 # veergude summa

col = len(open(filename, "r").readline().strip().split(";")) # Lühike

"""
________Pikk____________
f = open(filename, "r")
Line = f.readline()
Line = line.strip()
parts = line.split(";")
col = len(parts)
f.close()
________________________
"""

#print(col)

column = int(input(f"Sisesta veeru number: [1 - {col}] : "))
if column > 0 and column <= col:
    column -= 1
    with open(filename, "r") as f:
        contents = f.readlines() # Loe faili sisu muutujasse contents
        for line in contents:
            line = line.strip() # Eemaldab reavahetuse  /n
            parts = line.split(";") # Tükkelda rida semikoolonist
            if parts[column].isdigit(): # kas kõik kolm märki on numbrid
                total += int(parts[column])

        print(total) # lõpp tulemus
else:
    print(f"Vale veeru number, Lubatud on 1 - {col}")