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

def generuj_tajne_cislo(length=4):
    cislice = list(range(10))
    cislice.remove(0) 
    random.shuffle(cislice)
    return ''.join(map(str, cislice[:4]))

def ohodnot_tah(tajne_cislo, tip):
    bulls = 0
    cows = 0

    for i, cislice in enumerate(tajne_cislo):
        if tip[i] == cislice:
            bulls += 1
        elif tip[i] in tajne_cislo:
            cows += 1

    return bulls, cows

def hra():
    pozdrav()
    tajne_cislo = generuj_tajne_cislo()
    pokusy = 0

    while True:
        tip = input("Enter a number:\n>>> ")

        if not tip.isdigit():
            print("Invalid input. Please enter a 4-digit number.")
            continue
        elif len(tip) != 4:
            print("Invalid input. The number must have exactly 4 digits.")
            continue
        elif len(set(tip)) != 4:
            print("Invalid input. Digits must be unique.")
            continue
        elif tip[0] == '0':
            print("Invalid input. The number cannot start with zero.")
            continue

        bulls, cows = ohodnot_tah(tajne_cislo, tip)

        if bulls == 0 and cows == 0:
            print("No bulls or cows. None of the guessed digits are correct.")
        else:
            print(f"{bulls} {'bull' if bulls == 1 else 'bulls'}, {cows} {'cow' if cows == 1 else 'cows'}")

        pokusy += 1

        if bulls == 4:
            print(f"Correct, you've guessed the right number in {pokusy} {'guess' if pokusy == 1 else 'guesses'}!")
            break

if __name__ == "__main__":
    hra()
