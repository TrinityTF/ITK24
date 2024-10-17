# Funktsioonid
def showMessage():
    print("Tere tulemast!")

def welcome(name):
    print(f"Tere {name}!")

def calculate(a,b,c):
    return a+b+c
showMessage() # Kasuta funktsiooni
# welcome(input("Sisesta enda nimi: ").capitalize())
print(calculate(1,2,3))
result = calculate(4,6,2)
print(result)
print(calculate(result,result,result))
# Error: result2 = calculate(result,"result", 5)


"""
Kirjuta funktsioon mis tervitab ette antud nime 3 korda
"""
def tervitab(name):
    for i in range(3):
        print(f"Tere {name.capitalize()}!")

# tervitab(input("Sisesta enda nimi: "))

