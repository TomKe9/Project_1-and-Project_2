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

def extrahovat_info_o_hlasovani(zpracovana_url: list) -> list:
    # Extrahování informací o hlasování
    volici_v_seznamu = []
    vydane_obalky = []
    platne_hlasy = []
    kandidujici_strany = []

def zpracuj_data(zpracovana_url):
    volici_v_seznamu = []
    vydane_obalky = []
    platne_hlasy = []
    kandidujici_strany = []

    for url in zpracovana_url:
        volici = int(url.find("td", {"class": "cislo"}, headers="sa2").get_text().replace("\xa0", ""))
        volici_v_seznamu.append(volici)

        obalka = int(url.find("td", {"class": "cislo"}, headers="sa3").get_text().replace("\xa0", ""))
        vydane_obalky.append(obalka)

        hlas = int(url.find("td", {"class": "cislo"}, headers="sa6").get_text().replace("\xa0", ""))
        platne_hlasy.append(hlas)

        hlasy = url.find_all("td", headers=["t1sb3", "t2sb3"])
        kazda_stranicka_hlasy = [int(h.get_text().replace("\xa0", "")) for h in hlasy if h.get_text().strip() != "-"]
        kandidujici_strany.append(kazda_stranicka_hlasy)

    return volici_v_seznamu, vydane_obalky, platne_hlasy, kandidujici_strany

def ziskat_url(soup: BeautifulSoup) -> list:
    # Získání seznamu URL z HTML
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
    # Zpracování každé URL a vytvoření úplné URL pro zpracování
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
    # Zápis dat do CSV souboru
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