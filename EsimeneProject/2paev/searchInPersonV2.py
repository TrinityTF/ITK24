
filename = "Persons.csv"
total = 0 # Kui palju leiti

phrase = input("Sisesta fraas: (min. 2 märki)")

if len(phrase) > 1:
    f = open(filename, "r", encoding="utf-8")
    contents = f.readlines()[1:]
    f.close()
    for line in contents:
        line = line.strip() # Korrastab rea
        if phrase.lower() in line.lower():
            total += 1
            print(line)
    print(f"Leiti {total} rida")
else:
    print("Fraas liiga lühike")
