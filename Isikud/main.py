from Person import Person

if __name__ == '__main__':
    marko = Person("Marko","R","31.12.1999")
    anonymous = Person("Anonymous","?")
    print(marko.birth.year)
    print(anonymous.birth)
    print(marko.birth.strftime("%d.%m.%Y"))
    print(marko.calculate_age())
    print(anonymous.calculate_age())