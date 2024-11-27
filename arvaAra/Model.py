import random


class Model:
    def __init__(self):
        self.pc_nr = random.randint(1, 100)
        self.steps = 0
        self.gameOver = False
        self.filename = "result.txt"

    def ask(self):
        userNum = int(input("Sisesta number: "))
        self.steps += 1 # +1

        if userNum == 1000:
            print(f"Leidsid nõrga koha. Õige number on {self.pc_nr}.")
            self.gameOver = True
        elif userNum > self.pc_nr:
            print("Väiksem")
        elif userNum < self.pc_nr:
            print("Suurem")
        elif userNum == self.pc_nr:
            print(f"Leidisd õige arvu {self.steps} käiguga.")
            self.gameOver = True

    def letsPlay(self): # Küsib numbrit kuni mäng läbi
        while not self.gameOver:
            self.ask()

        name = self.askName()
        self.addNameToFile(name)

    def askName(self):
        name = input("Sisesta enda nimi: ")
        if not name.strip():
            name = "Anonymous"
        return name

    def addNameToFile(self, name):
        with open(self.filename, "a", encoding="utf-8") as file:
            line = f"{name};{self.pc_nr};{self.steps}\n"
            file.write(line)

