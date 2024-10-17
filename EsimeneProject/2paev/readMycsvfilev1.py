# read my csv file v1

filename = "Create-MyCSV-v.csv"
column = 0 # esimene veerg
total = 0 # veergude summa

with open(filename, "r") as f:
    contents = f.readlines() # Loe faili sisu muutujasse contents
    for line in contents:
        line = line.strip() # Eemaldab reavahetuse  /n
        parts = line.split(";") # Tükkelda rida semikoolonist
        if parts[column].isdigit(): # kas kõik kolm märki on numbrid
            total += int(parts[column])

    print(total) # lõpp tulemus

