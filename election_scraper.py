import requests as r
from bs4 import BeautifulSoup as bs
import csv
import sys

odkaz_prvni_cast = "https://volby.cz/pls/ps2017nss/"


def ziskej_odpoved(odkaz: str):
    return r.get(odkaz)


def soup_generator(response) -> str:
    if response.status_code == 200:
        html_text = response.text
        return bs(html_text, "html.parser")
    return ""


def hledej_tabulky(cont: str) -> str:
    return cont.find_all("table", {"class" : "table"})


def hledej_radky(table):
    return table.find_all("tr")


def najdi_hodnoty_obec(row: str) -> dict:
    try:
        number = row.find_all("td")[0].text
        name = row.find_all("td")[1].text
        link = row.find_all("a")[0]["href"]
        return ({"Cislo obce" : number, "Nazev obec" : name, "url" : link})
    except IndexError:
        pass


def ziskej_vstupni_info(tabs: str) -> list:
    info_list = []
    for tab in tabs:
        lines = hledej_radky(tab)
        for line in lines:
            info_list.append(najdi_hodnoty_obec(line))
    while None in info_list:
        info_list.remove(None)
    return info_list


def ziskej_odkaz(i : int, list_obci : list) -> str:
    return list_obci[i]["url"]


def rozdel_tabulky(soup:  str) -> str:
    tabulky_a = hledej_tabulky(soup)[0]
    tabulky_b = hledej_tabulky(soup)[1:]
    return tabulky_a, tabulky_b


def najdi_hodnoty_volby(row: str) -> dict:
    try:
        volici = row.find_all("td")[3].text.replace("\xa0","")
        vydane_obalky = row.find_all("td")[4].text.replace("\xa0","")
        ucast = row.find_all("td")[5].text
        odevzdane_obalky = row.find_all("td")[6].text.replace("\xa0","")
        platne_hlasy = row.find_all("td")[7].text.replace("\xa0","")
        return ({"Volici v seznamu" : volici, "Vydane obalky" : vydane_obalky, "Volebni ucast v %" : ucast,
                     "Odevzdane obalky" : odevzdane_obalky, "Platne hlasy" : platne_hlasy
                })
    except IndexError:
        pass


def ziskej_info_volby(tab: str) -> list:
    info_list = []
    lines = hledej_radky(tab)
    for line in lines:
        info_list.append(najdi_hodnoty_volby(line))
    while None in info_list:
        info_list.remove(None)
    return info_list


def najdi_hodnoty_strany(row: str) -> str:
    try:
        strana = row.find_all("td")[1].text
        pl_hlasy = row.find_all("td")[2].text.replace("\xa0","")
        return strana, pl_hlasy
    except IndexError:
        pass


def ziskej_info_strany(tabs: str) -> dict:
    info_dict = {}
    for tab in tabs:
        lines = hledej_radky(tab)
        for line in lines:
            if najdi_hodnoty_strany(line) == None:
                continue
            else:
                (key, value) = najdi_hodnoty_strany(line)
                info_dict.setdefault(key,value)
#    while None in info_list:
#        info_list.remove(None)
    return info_dict


def zapis_header_do_souboru(soubor: str, strany: list) -> list:
    header = ["Cislo obce",
              "Nazev obec",
              "Volici v seznamu",
              "Vydane obalky",
              "Volebni ucast v %",
              "Odevzdane obalky",
              "Platne hlasy",
              *strany
             ]
    f = open(soubor, 'w+', newline = '')
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    f.close()
    return header


def zapis_radky_do_souboru(soubor: str, header: list, slovnik_dat: dict) -> None:
    f = open(soubor, 'a', newline = '')
    writer = csv.DictWriter(f, header)
    writer.writerow(slovnik_dat)
    f.close()


def generuj_slovnik_dat_pro_zapis(slovnik_obec: dict, slovnik_volby: dict, slovnik_strany: dict) -> dict:
    slovnik_pro_zapis = {}
    slovnik_pro_zapis.update(slovnik_obec)
    slovnik_pro_zapis.update(slovnik_volby)
    slovnik_pro_zapis.update(slovnik_strany)
    slovnik_pro_zapis.pop("url")
    return slovnik_pro_zapis


def hlavni(adresa, jmeno_souboru):
    print(f"Stahuji data z URL: {adresa} .")
    response = ziskej_odpoved(adresa)
    soup = soup_generator(response)
    tabulky = hledej_tabulky(soup)
    list_info_hodnot = ziskej_vstupni_info(tabulky)
    print("Ukladam data do souboru...")
    for i in range(len(list_info_hodnot)):
        odkaz_obec = odkaz_prvni_cast + ziskej_odkaz(i, list_info_hodnot)
        response_obec = ziskej_odpoved(odkaz_obec)
        soup_obec = soup_generator(response_obec)
        tabulka_volby, tabulky_strany = rozdel_tabulky(soup_obec)
        list_info_volby = ziskej_info_volby(tabulka_volby)
        dict_info_strany = ziskej_info_strany(tabulky_strany)
        hlavni_slovnik = generuj_slovnik_dat_pro_zapis(list_info_hodnot[i], list_info_volby[0], dict_info_strany)
        if i == 0:
            header = zapis_header_do_souboru(jmeno_souboru, list(dict_info_strany.keys()))
            zapis_radky_do_souboru(jmeno_souboru, header, hlavni_slovnik)
        else:
            zapis_radky_do_souboru(jmeno_souboru, header, hlavni_slovnik)
    print("Ukoncuji Web Scraper.")


if __name__ == '__main__':
    adresa = sys.argv[1]
    jmeno_souboru = sys.argv[2]
    hlavni(adresa, jmeno_souboru)
