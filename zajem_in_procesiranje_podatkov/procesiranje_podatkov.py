import os
import re
import csv
import geonamescache as gc
import html

gc_objekt = gc.GeonamesCache()
countries = gc_objekt.get_countries()

drzave = [drzava["name"] for drzava in countries.values()]
drzave.sort(key=len, reverse=True) #zato da najprej ujame drzave ki so daljse, npr. South Sudan pred Sudan
drzave_re = "|".join(drzave)

pot_do_mape = "surovi_podatki"
def podrobnosti_o_jezikih():
    vsi_podatki = []

    for stran in os.listdir(pot_do_mape):
        pot = os.path.join(pot_do_mape, stran)
        with open(pot, encoding="utf-8") as d:
            vsebina = d.read()

            jezik = stran[:-4].strip().capitalize() #vse imajo na koncu ali .htm ali .php, veliko lazje kot iskanje z regex,
            # saj bi bilo treba upostevati se vse cudne znake

            re_koliko = re.search(r"about\s([\d,-.]+)", vsebina)
            if re_koliko:
                koliko = re_koliko.group(1).strip()
            else:
                koliko = "Extinct" if "extinct" in vsebina.lower() else "Unknown"

            re_kje = re.search(rf"(?:in|spoken in|parts of)\s+.*?({drzave_re})\b", vsebina, re.IGNORECASE) #IGNORECASE je za to, da je vseeno ali 
            # so velike ali male črke, ne gre z vsebina.lower(), saj moramo gledati v slovarju kjer so drzave napisane z veliko zacetnico
            if re_kje:
                kje = re_kje.group(1).strip()
            else:
                kje = "Unknown"

            re_druzina = re.search(r"(?:belongs to the|member of the|part of the|the)\s+([A-Z][a-zA-Z- ]+?)\s+(?:branch|language family|family)", vsebina)
            if re_druzina:
                druzina = re_druzina.group(1).strip()
            else:
                druzina = "Unknown"

            re_pisava = re.search(r"\b(?!(?:Constructed|Alternative)\b)([A-Z][a-z]+?)\s+(?:script|alphabet)", vsebina)
            if re_pisava:
                pisava = re_pisava.group(1).strip()
            else:
                re_pisava_alt = re.search(r"written with the\s+([A-Z][a-z]+)", vsebina)
                pisava = re_pisava_alt.group(1).strip() if re_pisava_alt else "Unknown"

            re_primer_povedi = re.search(r"Sample text.+?<(?:p|li)>(.+?)</(?:p|li)>", vsebina, re.DOTALL | re.IGNORECASE) #DOTALL je da gleda cez vec vrstic, ne pa
            # samo eno, saj so nekatere znacke cez vec vrstic pri primerih povedi, vcasih se pojavi pod p vcasih pod li znacko
            if re_primer_povedi:
                surov_tekst = re_primer_povedi.group(1)
                if "http" in surov_tekst or "Source:" in surov_tekst:
                    primer_povedi = "None"
                else:
                    cist_primer = re.sub(r"<[^>]+>", "", surov_tekst) #zbrisejo se razne znacke, ki se lahko prikradejo v poved
                    cist_primer = html.unescape(cist_primer) #cudne znake pretvorimo v lepe
                    cist_primer = re.sub(r'\s+', ' ', cist_primer) #odstranimo skoke v novo vrstico
                    if cist_primer.strip():  
                        primer_povedi = cist_primer.strip()
                    else:
                        primer_povedi = "None"
            else:
                primer_povedi = "None"

            vsi_podatki.append({
                            "jezik": jezik,
                            "govorci": koliko,
                            "drzava": kje,
                            "druzina": druzina,
                            "pisava": pisava,
                            "primer povedi": primer_povedi
                        })
    return vsi_podatki


os.makedirs("podatki", exist_ok=True)
koncni_podatki = podrobnosti_o_jezikih()
pot_do_csv = os.path.join("podatki", "podatki.csv")

with open("podatki/podatki.csv", "w", encoding="utf-8", newline="") as c:
    pisatelj = csv.writer(c)
    pisatelj.writerow(
        [
            "jezik",
            "govorci",
            "drzava",
            "druzina",
            "pisava",
            "primer povedi"
        ]
    )

    for vrstica in koncni_podatki:
            pisatelj.writerow(
                [
                    vrstica["jezik"],
                    vrstica["govorci"],
                    vrstica["drzava"],
                    vrstica["druzina"],
                    vrstica["pisava"],
                    vrstica["primer povedi"]
                ]
            )




