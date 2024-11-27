import random


class Model:

    # Klassi muutujad
    pc_nr = 0
    steps = 0
    gameOver = False

    def __init__(self):
        self.gameReset()
        self.filename = "result.txt"

    def gameReset(self):
        self.pc_nr = random.randint(1, 100)
        self.steps = 0
        self.gameOver = False

    def ask(self):
        user = int(input("Sisesta number: "))
        self.steps += 1 # +1

        if user == 1000:
            print(f"Leidsid nõrga koha. Õige number on {self.pc_nr}.")
            self.gameOver = True
        elif user > self.pc_nr:
            print("Väiksem")
        elif user < self.pc_nr:
            print("Suurem")
        elif user == self.pc_nr:
            print(f"Leidisd õige arvu {self.steps} käiguga.")
            self.gameOver = True

    def letsPlay(self): # Küsib numbrit kuni mäng läbi
        while not self.gameOver:
            self.ask()

        name = self.askName()
        self.addNameToFile(name)

        if self.playAgain():
            self.gameReset()
            self.letsPlay()

    def askName(self):
        name = input("Sisesta enda nimi: ")
        if not name.strip():
            name = "Anonymous"
        return name

    def addNameToFile(self, name):
        with open(self.filename, "a", encoding="utf-8") as file:
            line = f"{name};{self.pc_nr};{self.steps}\n"
            file.write(line)

    def playAgain(self):
        user = input("Kas mängid uuesti? [ Jah / Ei ]")
        if user.lower() == "jah" or user.lower() == "j":
            return True
        return False


