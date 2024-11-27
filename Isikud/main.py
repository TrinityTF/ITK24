from Person import Person

if __name__ == '__main__':
    marko = Person("Marko","R","31.12.1999")
    anonymous = Person("Anonymous","?")
    print(marko.birth.year)
    print(anonymous.birth)
    print(marko.birth.strftime("%d.%m.%Y"))
    print(marko.calculate_age())
    print(anonymous.calculate_age())
    print(marko)
    print(anonymous)

    print("_____________________________________")

    names = ["Heli Kopter","Jaana Lind", "Zoonja Puhur", "Niina Sarvik", "Maksim Market"]
    genders = ["N","N","","N","M"]
    dates =["01.01.1990", "", "31.12.2000", "30.11.2010", "05.07.1980"]

    """
    Loo listid mis sisaldab Person objekte (5 tk) mis on loodud listide names, gender ja dates põhjal.
    Näita loodud  listi sisu eraldi/tesie for-loopiga
    
    """
    # Uus list
    persons = []
    for name, gender, date in zip(names, genders, dates):
        persons.append(Person(name, gender, date))

    # Print for loop
    for person in persons:
        print(person)
