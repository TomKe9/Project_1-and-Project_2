**Engeto-pa-3-projekt**

Třetí projekt na Python Akademii od Engeta.

**Popis projektu**

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí zde: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ.

**Instalace knihoven**

Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Po instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustí následovně: 

**Spuštění projektu**

Spuštění souboru Python_3.py v rámci příkazového řádku požaduje dva povinné argumenty.

Následně se vám stáhnou výsledky jako soubor s příponou .csv

**Ukázka projektu**

Výsledky hlasování pro okres Trutnov:
1. argument: https://volby.cz/pls/ps2017nss/ps32xjazyk=CZ&xkraj=8&xnumnuts=5205
2. argument: vysledky_trutnov.csv

**Spuštění programu:**

python Projekt_3.py "https://volby.cz/pls ps2017nss/ps32xjazyk=CZ&xkraj=8&xnumnuts=5205" "vysledky_trutnov.csv"

**Průběh stahování:**

Začínám stahovat a zpracovávat data...

Zahajuji zápis do CSV souboru...

Soubor vysledky_trutnov.csv byl úspěšně vytvořen.

**Částečný výstup:**

kód_obce;název_obce;voliči v seznamu;vydané obálky;platné hlasy;...
