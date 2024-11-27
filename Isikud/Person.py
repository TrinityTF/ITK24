import datetime


class Person:

    def __init__(self, name, gender, birth=None):
        # Kuupäev on  kujul PP.KK.AAAA
        self.name = name
        self.gender = gender
        self.birth = None

        if birth:
            day, month, year = map(int, birth.split('.'))
            birthObj = datetime.date(year, month, day)
            self.birth = birthObj

    def calculate_age(self):
        if self.birth is not None:
            today = datetime.date.today()
            return today.year - self.birth.year - ((today.month, today.day) < (self.birth.month, self.birth.day))
        return None

    def __str__(self):
        # Väljasta kogu info isiku kohta
        return f"{self.name} {self.gender} {self.birth} {self.calculate_age()}"
