"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Tomáš Filipský
email: tomas.filipsky@email.cz
discord: tomas_53249
"""

import os
import requests
import csv
from bs4 import BeautifulSoup
import sys

def ziskat_odpoved(url: str) -> str:
    # Získání dat z URL
    odpoved = requests.get(url)
    return odpoved.text

def parsovat_odpoved(odpoved: str) -> BeautifulSoup:
    # Parsování odpovědi do formátu HTML
    soup = BeautifulSoup(odpoved, "html.parser")
    return soup

def ziskat_radky_tabulky(soup: BeautifulSoup) -> list:
    # Získání potřebných dat z HTML tabulky
    radky = soup.find_all("tr")
    radky_tabulky = [radek.get_text().strip().splitlines() for radek in radky]
    return radky_tabulky

def extrahovat_info_o_hlasovani(zpracovana_url):
    """
    Extrahuje informace o hlasování z webové stránky zpracované pomocí BeautifulSoup.

    Parametry:
    zpracovana_url (list): Seznam zpracovaných URL s informacemi o hlasování.

    Návratové hodnoty:
    tuple: Čtyři seznamy obsahující informace o hlasování.
        1. Seznam počtu voličů v seznamu.
        2. Seznam počtu vydání obálek.
        3. Seznam počtu platných hlasů.
        4. Seznam seznamů počtů hlasů pro každou kandidující stranu.

    Pokud není nalezena žádná data nebo jsou chybějící, funkce vrátí None.
    """
    volici_v_seznamu = []
    vydane_obalky = []
    platne_hlasy = []
    kandidujici_strany = []

    for url in zpracovana_url:
        volici = url.find("td", {"class": "cislo"}, headers="sa2").get_text()
        volici_v_seznamu.append(int(volici.replace("\xa0", "")))

        obalka = url.find("td", {"class": "cislo"}, headers="sa3").get_text()
        vydane_obalky.append(int(obalka.replace("\xa0", "")))

        hlas = url.find("td", {"class": "cislo"}, headers="sa6").get_text()
        platne_hlasy.append(int(hlas.replace("\xa0", "")))

        hlasy = url.find_all("td", headers=["t1sb3", "t2sb3"])
        kazda_stranicka_hlasy = []
        for hlas in hlasy:
            if hlas.get_text().strip() != "-":
                kazda_stranicka_hlasy.append(int(hlas.get_text().replace("\xa0", "")))
        kandidujici_strany.append(kazda_stranicka_hlasy)

    # Přesvědčte se, že máte správné návratové hodnoty
    if not volici_v_seznamu or not vydane_obalky or not platne_hlasy or not kandidujici_strany:
        return None
    
    return volici_v_seznamu, vydane_obalky, platne_hlasy, kandidujici_strany

def ziskat_url(soup: BeautifulSoup) -> list:
    """
    Získá seznam URL odkazů z objektu BeautifulSoup obsahujícího HTML stránku.

    Parametry:
    soup (BeautifulSoup): Objekt BeautifulSoup reprezentující zpracovanou HTML stránku.

    Návratová hodnota:
    list: Seznam URL odkazů.

    Funkce prochází tabulky na stránce a hledá odkazy v těchto tabulkách.
    Pokud odkaz obsahuje řetězec "vyber=" a není již v seznamu, přidá ho do seznamu.
    Nakonec vrátí tento seznam URL odkazů.
    """
    tabulky = soup.find_all('table')
    seznam_url = []
    for tabulka in tabulky:
        a_tagy = tabulka.find_all("a")
        for tag in a_tagy:
            odkaz = tag.get("href")
            if "vyber=" in odkaz and odkaz not in seznam_url:
                seznam_url.append(odkaz)
    return seznam_url

def ziskat_zpracovatelne_url(seznam_url: list) -> list:
    """
    Získá zpracovatelná URL zkrácením základní URL a připojením odkazů ze vstupního seznamu.

    Parametry:
    seznam_url (list): Seznam URL odkazů ke zpracování.

    Návratová hodnota:
    list: Seznam úplných URL k zpracování.

    Každá URL zkrácením o základní část zakladni_url a připojením URL ze vstupního seznamu.
    Funkce vrátí seznam těchto úplných URL, které jsou připraveny k zpracování.
    """
    zakladni_url = "https://volby.cz/pls/ps2017nss/"
    zpracovatelne_url = [zakladni_url + url for url in seznam_url]
    return zpracovatelne_url

def zpracovat_url(zpracovatelne_url: list) -> list:
    # Parsování a zpracování všech potřebných URL
    zpracovana_url = [parsovat_odpoved(ziskat_odpoved(url)) for url in zpracovatelne_url]
    return zpracovana_url

def ziskat_cislo_mesta(radky_tabulky: list) -> list:
    # Získání seznamu čísel a názvů měst
    seznam_cisel_mest = [podseznam[0] for podseznam in radky_tabulky[2:] if podseznam[0] not in ["-", "Obec", "číslo"]]
    return seznam_cisel_mest

def ziskat_nazev_mesta(radky_tabulky: list) -> list:
    # Získání seznamu názvů měst
    seznam_nazvu_mest = [podseznam[1] for podseznam in radky_tabulky[2:] if podseznam[1] not in ["název", "Výběrokrsku", "-"]]
    return seznam_nazvu_mest

def ziskat_nazvy_politickych_stran(soup: BeautifulSoup) -> list:
    # Získání seznamu názvů politických stran
    td_tagy = soup.find_all("td", {"class": "overflow_name"})
    politicka_strana = [tag.get_text() for tag in td_tagy]
    return politicka_strana

def hlavni(url: str):
    """
    Hlavní funkce pro zpracování informací o výsledcích voleb z webové stránky.

    Parametry:
    url (str): Adresa URL stránky obsahující informace o výsledcích voleb.

    Návratová hodnota:
    dict: Slovník obsahující záhlaví CSV souboru a data pro zápis.

    Funkce provede následující kroky:
    1. Získá odpověď z webového serveru pro zadanou URL.
    2. Zpracuje odpověď pomocí parsování do objektu BeautifulSoup.
    3. Získá řádky tabulky obsahující informace o výsledcích voleb.
    4. Extrahuje kódy a názvy měst z tabulky.
    5. Získá seznam URL odkazů na podrobnější informace o výsledcích voleb.
    6. Získá úplné zpracovatelné URL odkazy.
    7. Zpracuje URL a extrahuje informace o hlasování.
    8. Získá názvy politických stran.
    9. Vytvoří záhlaví CSV souboru.
    10. Vytvoří data pro zápis do CSV.

    Návratová hodnota je slovník obsahující záhlaví CSV souboru a data pro zápis.
    """
    odpoved = ziskat_odpoved(url)
    soup = parsovat_odpoved(odpoved)
    radky_tabulky = ziskat_radky_tabulky(soup)
    kody_mest = ziskat_cislo_mesta(radky_tabulky)
    nazvy_mest = ziskat_nazev_mesta(radky_tabulky)
    url_adresy = ziskat_url(soup)
    zpracovatelne_url = ziskat_zpracovatelne_url(url_adresy)
    zpracovana_url = zpracovat_url(zpracovatelne_url)
    pocet_volicu, pocet_obalek, pocet_platnych_hlasu, vsechny_stranicke_hlasy = extrahovat_info_o_hlasovani(zpracovana_url)
    strany = ziskat_nazvy_politickych_stran(zpracovana_url[0])

    # Vytvoření záhlaví CSV souboru
    zahlavi = ["kód_obce", "název_obce", "voliči v seznamu", "vydané obálky", "platné hlasy", *strany]

    # Vytvoření dat pro zápis do CSV
    data = [[kod, nazev, volici, obalky, platne_hlasy, *hlasy] for kod, nazev, volici, obalky, platne_hlasy, hlasy in
            zip(kody_mest, nazvy_mest, pocet_volicu, pocet_obalek, pocet_platnych_hlasu, vsechny_stranicke_hlasy)]

    return {"zahalvi": zahlavi, "data": data}

def do_csv(nazev_souboru: str, data):
    """
    Zápis dat do CSV souboru.

    Parametry:
    nazev_souboru (str): Název CSV souboru, do kterého se mají data zapsat.
    data (dict): Slovník obsahující záhlaví CSV souboru a data pro zápis.

    Funkce zapisuje data do CSV souboru se zadaným názvem. Pokud soubor již existuje, bude přepsán.

    Pokud se při zápisu do souboru vyskytne chyba oprávnění, funkce vypíše chybové hlášení a ukončí běh programu.
    """
    try:
        with open(nazev_souboru, mode="w", encoding="utf-8-sig", newline="") as soubor:
            writer = csv.writer(soubor, delimiter=";")
            writer.writerow(data["zahalvi"])
            for radek in data["data"]:
                writer.writerow(radek)

    except PermissionError:
        print("Odmítnuto oprávnění.\n"
              "Zkontrolujte a spusťte znovu.")
        exit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Vlož dva argumenty: odkaz a soubor")
        sys.exit(1)

    odkaz, nazev_souboru = sys.argv[1], sys.argv[2]

    print("Začínám stahovat a zpracovávat data...\n"
          "Zahajuji zápis do CSV souboru...")
    data = hlavni(odkaz)
    do_csv(nazev_souboru, data)
    print(f"Soubor {nazev_souboru} byl úspěšně vytvořen.")
    exit()