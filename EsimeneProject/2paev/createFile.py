"""
Küsi kasutajalt mõned nimed. Min 2.
Mitme nime puhul kasutatakse nimede vahel tühikut.
TÄIENDUS: Vähemalt kaks tähte ja ainult tähed, siis lisab failid
"""

filename = "CreateCSV.txt"

separator = " " # Nimede eraldaja
total = 0

userInput = input("Sisesta mitu nime, eraldaja tühik: ")
if len(userInput.split(separator)) > 1:
    print(userInput)
    parts = userInput.split(separator)
    src = open(filename, "a", encoding="utf-8")
    for part in parts:
        if len(part) > 1 and part.isalpha():
            src.write(part + "\n")
            total += 1
        else:
            print(f"Ei saa kirjutada: {part} ")
    print(f"Kirjutati {total} nime.")

    src.close()
else:
    print("Vale input")