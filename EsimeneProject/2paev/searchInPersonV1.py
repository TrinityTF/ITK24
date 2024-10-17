import csv

filename = "Persons.csv"

phrase = input("Sisesta otsitav fraas: (min. 2 märki)")

if len(phrase) > 1:
    # pass
    with open(filename, "r", encoding="utf-8") as f:
        contents = csv.reader(f, delimiter=";")
        for row in contents:
            if phrase.lower() in row[0].lower() or phrase.lower() in row[1].lower():
                print(";".join(row))
else:
    print("Fraas on liiga lühike")