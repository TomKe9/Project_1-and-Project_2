"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Tomáš Filipský
email: tomas.filipsky@email.cz
discord: tomas_53249
"""

import re

# zaregistrovaní uživatelé
registrovani_uzivatele = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

TEXTS = [
    '''
    Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30N and the Union Pacific Railroad,
    which traverse the valley. 
    ''',
    '''
    At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.
    ''',
    '''
    The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.
    '''
]

# přihlášení uživatele
username = input("username:")
password = input("password:")

# ověření uživatele
if username in registrovani_uzivatele and registrovani_uzivatele[username] == password:
    print(f"Welcome to the app, {username}")
    print(f"We have {len(TEXTS)} texts to be analyzed.")
else:
    print("Unregistered user, terminating the program...")
    exit()

# Ověření uživatelova vstupu pro výběr textu
while True:
    selected_text = input(f"Enter a number between 1 and {len(TEXTS)} to select: ")
    if selected_text.isdigit():
        selected_text = int(selected_text)
        if 1 <= selected_text <= len(TEXTS):
            break
    print("Invalid input. Please enter a number between 1 and", len(TEXTS))

selected_text = selected_text - 1
text = TEXTS[selected_text]

# Tokenizace textu s odstraněním teček a čárek
words = re.findall(r'\b\w+\b', text)

word_count = 0
titlecase_words = 0
uppercase_words = 0
lowercase_words = 0
numeric_strings = 0
numeric_sum = 0
word_lengths = {}

for word in words:
    # Počet slov
    word_count += 1
    
    # Počet slov začínajících velkým písmenem
    if word.istitle():
        titlecase_words += 1
        
    # Počet slov psaných velkými písmeny
    if word.isupper() and word.isalpha():
        uppercase_words += 1
        
    # Počet slov psaných malými písmeny
    if word.islower():
        lowercase_words += 1
    
    # Počet čísel
    if word.isdigit():
        numeric_strings += 1
        numeric_sum += int(word)
    
    # Délka slova
    word_length = len(word)
    if word_length in word_lengths:
        word_lengths[word_length] += 1
    else:
        word_lengths[word_length] = 1

print(f"There are {word_count} words in the selected text.")
print(f"There are {titlecase_words} titlecase words.")
print(f"There are {uppercase_words} uppercase words.")
print(f"There are {lowercase_words} lowercase words.")
print(f"There are {numeric_strings} numeric strings.")
print(f"The sum of all the numbers {numeric_sum}")

# Graf
print("\nLEN|  OCCURRENCES  |NR.")
print("-" * 25)
for length in range(1, max(word_lengths.keys()) + 1):
    occurrences = word_lengths.get(length, 0)
    print(f"{length:3}|{'*' * occurrences:<17}|{occurrences}")
