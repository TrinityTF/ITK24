"""
Ülesanne:
    1. Juhuslik nimi failist, mitte et te valite sobivad nimed endale koodi!
    2. Esimene number on juhuslik vahemikus 1 – 100 k.a.
    3. Teine number on juhuslik vahemikus 1 – 30. Kui arvuks tuleb number 1, 2 või 3 siis teatab lisaks muule infole konsooli ka "Õnneseen" (vaata Sele 2). 
    Faili seda teksti Õnneseen ei kirjutata (vaata Sele 1)
    4. See mitu kirjet/rida korraga lisada küsitakse kasutajalt ja see on lubatud vahemikus 5 - 10 k.a. (vaata Sele 3). Vaata ka punkt 6.
    5. Jagatud faili (Eesnimed.csv) nime ja sisu ei tohi muuta.
    6. Kui punktis 4 sisestatud number on vale, siis informeeritakse kasutajat vigasest sisendist ja midagi faili ei lisata.
    7. Konsooli ja failiinfo:
        a. Kolme veeru järjekord on: Nimi, Number 1-100, Number 1-30, Õnneseen
        b. Konsooli näidatakse kolm veergu eraldajaks tühik (neljas veerg, siis kui on ka tekst Õnneseen)
        c. Faili kirjutatakse alati kolm veergu eraldajaks semikoolon.
    8. Lisa punkt:
        a. Väljasta konsooli info nagu paistab Sele 4. Nime jaoks on 15 kohta, esimese numbri jaoks on 3 kohta ja viimase numbri jaoks on 2 kohta
        b. Faili sisu ei muutu sellest (vaata Sele 5).
        c. Väljastuseks jääb ainult üks variant. Kas algne nagu Sele 2 või vormindatud nagu Sele 4. Ära näita/-kasuta mõlemat varianti sama aegselt.
    9. Tehtava faili nimi on result.txt
        a. Fail ei sisalda päist. Algab kohe andmetega
    10. Teamsi ülesande juurde tuleb jagada ainult Pythoni fail. Failinimi peab sisaldama teie eesnime!
"""
import csv
import random

# Eesnimed.csv faili lugemine ja nimede listi tegemine
with open("Eesnimed.csv", newline="", encoding="utf-8") as csvfile:
    r = csv.reader(csvfile, delimiter=';')  
    nimed = [row[1] for row in r]  

def ranNum100():  # Suvaline number 1-100 vahel
    return random.randint(1, 100)

def ranNum30():  # Suvaline number 1-30 vahel
    return random.randint(1, 30)

def kasutajaNumber():  # Kasutaja input
    while True:
        try:
            number = int(input("Mitu nime näitame: (5 - 10) "))
            if 5 <= number <= 10:
                return number
            else:
                print("Vale number! Sisesta number vahemikus 5 - 10.")
        except ValueError:
            print("Vale number! Sisesta täisarv.")

def failiKirjutamine(arv):  # Tulemuste faili lisamine ja konsoolis näitamine
    with open("result.txt", "a", newline="", encoding="utf-8") as resultfile:
        w = csv.writer(resultfile, delimiter=";")
        for _ in range(arv):
            nimi = random.choice(nimed)  # Valib juhusliku nime
            num100 = ranNum100()
            num30 = ranNum30()

            # Kui num30 on 1, 2 või 3, siis lisab Õnneseen'e
            if num30 in [1, 2, 3]:
                print(f"{nimi:<15} {num100:>3} {num30:>2} Õnneseen")
            else:
                print(f"{nimi:<15} {num100:>3} {num30:>2}")

            # Kirjutame tulemused faili 
            w.writerow([nimi, num100, num30])

# Funktsioonide kasutamine
arv = kasutajaNumber()
failiKirjutamine(arv)
