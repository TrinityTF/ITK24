import random


class Model:
    def __init__(self):
        self.pc_nr = random.randint(1, 100)
        self.steps = 0
        self.gameOver = False

    def ask(self):
        userNum = int(input("Sisesta number: "))
        self.steps += 1 # +1

        if userNum > self.pc_nr:
            print("Väiksem")
        elif userNum < self.pc_nr:
            print("Suurem")
        elif userNum == self.pc_nr:
            print(f"Leidisd õige arvu {self.steps} käiguga.")
            self.gameOver = True

    def letsPlay(self): # Küsib numbrit kuni mäng läbi
        while not self.gameOver:
            self.ask()