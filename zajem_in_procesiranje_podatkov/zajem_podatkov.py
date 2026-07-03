import requests
import re

url = "https://www.omniglot.com/writing/languages.htm"
HEADERS = {"User-Agent": "Mozilla/5.0"} #rabimo saj, drugace vrne statusno kodo 403
odgovor = requests.get(url, headers=HEADERS)
surova_koda = odgovor.text

def podrobnosti_o_jezikih(vsebina):
    vsi_linki = re.findall(r'<a href="(.+\.(?:htm|php|htm#ls|htm#us))".+>', vsebina) #""?:"" pomeni, da so tisti oklepaji nezajemalni
    nerelevantno = ['index', 'about', 'contact', 'search', 'news', 'copyright', 
                  'donations', 'advertising', 'sitemap', 'links', 'books', 
                  'gallery', 'puzzles', 'faqs', 'media', 'events'
                  'writing', 'language', 'frantastique', 'langfam']
    vsi_jeziki = [link for link in vsi_linki if not any(beseda in link.lower() 
                                                           for beseda in nerelevantno)]
    print(vsi_jeziki)
    print(len(vsi_jeziki))