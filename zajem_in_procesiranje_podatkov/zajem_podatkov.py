import os
import requests
import re
import time
import shutil

url = "https://www.omniglot.com/writing/languages.htm"
HEADERS = {"User-Agent": "Mozilla/5.0"} #rabimo saj, drugace vrne statusno kodo 403
vsebina = requests.get(url, headers=HEADERS)
surova_koda = vsebina.text

def podrobnosti_o_jezikih(vsebina):
    vsi_linki = re.findall(r'<a href="(.+\.(?:htm|php|htm#ls|htm#us))".+>', vsebina) #""?:"" pomeni, da so tisti oklepaji nezajemalni
    nerelevantno = ['index', 'about', 'contact', 'search', 'news', 'copyright', 
                  'donations', 'advertising', 'sitemap', 'links', 'books', 
                  'gallery', 'puzzles', 'faqs', 'media', 'events', 
                  'writing', 'language', 'frantastique', 'langfam']
    vsi_jeziki = [re.sub(r"^\.\./", "", link) for link in vsi_linki if not any(beseda in link.lower() 
                                                           for beseda in nerelevantno)] #sub je za tiste linke ki imajo na zacetku ""../""

    if os.path.exists("surovi_podatki"):
            shutil.rmtree("surovi_podatki") #izbrise mapo surovi_podatki
    os.makedirs("surovi_podatki", exist_ok=True) #jo se enkrat ustvari
    
    for i in vsi_jeziki:
        if i == "daao.htm":
            i = "daai.htm" #napaka na spletni strani
        if "chinese" in i:
            podrobnosti = requests.get("https://www.omniglot.com/" + i, headers=HEADERS)
        else:
            podrobnosti = requests.get("https://www.omniglot.com/writing/" + i, headers=HEADERS)
        if "chinese" in i: #problemi z jeziki ki so bili napisani pod en jezik
            pot = os.path.join("surovi_podatki", i[8:]) #""chinese/"" ima 8 znakov
        else:
            pot = os.path.join("surovi_podatki", i)
        if podrobnosti.status_code == 200:
            with open(pot, "w", encoding="utf-8") as d:
                d.write(podrobnosti.text)
        else:
            print(f"Prišlo je do napake pri url-ju za jezik: {i}.")
        time.sleep(0.5)