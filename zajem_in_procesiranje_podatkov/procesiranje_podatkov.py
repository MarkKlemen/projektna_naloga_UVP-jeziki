import os
import re
import csv
import geonamescache as gc

countries = gc.get_countries()
drzave = [drzava["name"] for drzava in countries.values()]
drzave_re = "|".join(drzave)

pot_do_mape = "surovi_podatki"
def podrobnosti_o_jezikih():
    for stran in os.listdir(pot_do_mape):
        pot = os.path.join(pot_do_mape, stran)
        with open(pot, encoding="utf-8") as d:
            vsebina = d.read()
            jezik = re.search(r"<title>(.+) language", vsebina)
            if re.search(r"about\s([\d,]+)", vsebina):
                koliko = re.search(r"about\s([\d,]+\speople)", vsebina)
            else:
                koliko = "Extinct"
            kje = re.search(rf"in\s({drzave_re}))", vsebina)
            jezikovna_druzina = re.search(r"(?:the\s(.+)\slanguage family|(is a member of the\s(.+?))|is part of the\s(.+?))", vsebina)
            pisava = re.search(r"(.+?)\salphabet", vsebina)
            






