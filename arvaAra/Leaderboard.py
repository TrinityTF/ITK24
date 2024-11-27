class Leaderboard:

    def __init__(self, name, number, steps):
        self.name = name
        self.number = number
        self.steps = steps

    def __str__(self):
        return f"{self.name:20} {self.number:3} {self.steps:2}"