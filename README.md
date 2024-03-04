**Engeto-pa-3-projekt**

Třetí projekt na Python Akademii od Engeta.

**Popis projektu**

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí zde: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ .

**Instalace knihoven**

Knihovny, které jsou přidány do kódu jsou uložené v souboru requirements.txt. Po instalaci doporučuji použít nové virtuální prostředí jako následovně nainstalovaným manažerem spustí:

**Spuštění projektu**

Spuštění souboru Python_3.py v rámci příkazového řádku požaduje dva povinné argumenty. 

Nakonec se vám stáhnou výsledky jako soubor s příponou .csv

**Ukázka projektu**

Výsledky hlasování pro okres Trutnov:

argument: https://volby.cz/pls/ps2017nss/ps32xjazyk=CZ&xkraj=8&xnumnuts=5205
argument: vysledky_trutnov.csv

**Spuštění programu:**

python Projekt_3.py " https://volby.cz/pls ps2017nss/ps32xjazyk=CZ&xkraj=8&xnumnuts=5205" "vysledky_trutnov.csv"

**Průběh stahování:**

Začínám stahovat a zpracovávat data...

Zahajuji zápis do CSV souboru...

Soubor vysledky_trutnov.csv byl úspěšně vytvořen.

**Částečný výstup:**

kód_obce;název_obce;voliči v seznamu;vydané obálky;platné hlasy;... 
579041;Batňovice;635;415;414;53;0;0;20;0;10;27;3;1;5;0;1 ;44;1;8;133;1;0;46;1;1;0;58;1 
579050;Bernartice;725;441;439;41;0;0;26;0;15;54;3; 4;4;0;0;37;2;4;155;0;0;16;2;15;1;59;1 ...
