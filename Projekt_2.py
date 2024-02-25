"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Tomáš Filipský
email: tomas.filipsky@email.cz
discord: tomas_53249
"""

import random 

def pozdrav():
    print("Hi there!")
    print("-" * 25)
    print("I've generated a random 4 digit number for you.", "Let's play a bulls and cows game.", sep="\n")
    print("-" * 25)

def generuj_tajne_cislo(lenght=4):
    cislice = list(range(1, 10))  # Změna rozsahu na 1 až 9, aby se vyhnuli nule na začátku
    random.shuffle(cislice)
    return cislice[:4]

def ohodnot_tah(tajne_cislo, tip):
    bulls = 0
    cows = 0

    for i in range(len(tajne_cislo)):
        if int(tip[i]) == tajne_cislo[i]:
            bulls += 1
        elif int(tip[i]) in tajne_cislo and int(tip[i]) != tajne_cislo[i]:
            cows += 1

    return bulls, cows

def hra():
    pozdrav()
    tajne_cislo = generuj_tajne_cislo()
    pokusy = 0

    while True:
        tip = input("Enter a number:\n>>> ")

        if not tip.isdigit() or len(tip) != 4 or len(set(tip)) != 4 or tip[0] == '0':
            print("Invalid input. Please enter 4 unique digits.")
            continue

        bulls, cows = ohodnot_tah(tajne_cislo, tip)

        print(f"{bulls} {'bull' if bulls == 1 else 'bulls'}, {cows} {'cow' if cows == 1 else 'cows'}")

        pokusy += 1

        if bulls == 4:
            print(f"Correct, you've guessed the right number in {pokusy} {'guess' if pokusy == 1 else 'guesses'}!")
            break

if __name__ == "__main__":
    hra()
