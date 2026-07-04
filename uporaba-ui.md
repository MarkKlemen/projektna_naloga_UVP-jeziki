# 1. Kako v pythonu naredis novo mapo in kako lahko to mapo ob klicu funkcije najprej zbirses ter jo nato ponovno ustvaris? Ali za to obstaja kaksna knjiznica?

V Pythonu je delo z mapami (imeniki) zelo preprosto. Za to imamo na voljo dve odlični vgrajeni knjižnici: os (klasična pot) in pathlib (modernejša, bolj intuitivna pot). Za brisanje map, ki niso prazne, pa poleg njiju uporabimo še knjižnico shutil.

Za tvoj primer (izbriši, če obstaja, in nato ustvari znova) je najbolj elegantna uporaba knjižnice pathlib v kombinaciji s shutil.

Tukaj je celoten postopek in koda, kako to narediš.

Rešitev z modernim pathlib in shutil
To je trenutno najbolj priporočljiv način v Pythonu, saj z mapami delaš kot z objekti, koda pa je zelo čitljiva.

Python
from pathlib import Path
import shutil

def ponovno_ustvari_mapo(ime_mape: str):
    # Ustvarimo objekt Path za našo mapo
    pot = Path(ime_mape)
    
    # 1. Preverimo, če mapa že obstaja
    if pot.exists():
        # Če obstaja, jo izbrišemo (tudi če vsebuje datoteke)
        shutil.rmtree(pot)
        print(f"Mapa '{ime_mape}' je bila uspešno izbrisana.")
    
    # 2. Ustvarimo popolnoma novo, prazno mapo
    # parents=True omogoča, da ustvari vmesne mape, če ne obstajajo
    # exist_ok=True prepreči napako, če bi mapa slučajno že obstajala
    pot.mkdir(parents=True, exist_ok=True)
    print(f"Mapa '{ime_mape}' je bila uspešno ustvarjena.")

## Primer klica funkcije
ponovno_ustvari_mapo("moja_nova_mapa")
Alternativa s klasično knjižnico os
Če ti je bolj všeč klasični pristop, kjer z mapami upravljaš preko nizov (teksta), lahko uporabiš modul os. Logika ostaja popolnoma ista:

Python
import os
import shutil

def ponovno_ustvari_mapo_os(ime_mape: str):
    # 1. Preverimo in izbrišemo, če obstaja
    if os.path.exists(ime_mape):
        shutil.rmtree(ime_mape)
        print(f"Mapa '{ime_mape}' izbrisana.")
        
    # 2. Ustvarimo mapo znova
    os.makedirs(ime_mape, exist_ok=True)
    print(f"Mapa '{ime_mape}' ustvarjena.")

## Primer klica
ponovno_ustvari_mapo_os("stara_sola_mapa")
Ključne funkcije, ki si jih velja zapomniti:
shutil.rmtree(): Ključna funkcija, saj navadni os.rmdir() ali Path.rmdir() javita napako, če mapa ni popolnoma prazna. rmtree (remove tree) pa brez milosti pobriše mapo in vso njeno vsebino (datoteke in podmape).

exist_ok=True: Zelo koristen parameter pri ustvarjanju map, ki prepreči, da bi Python vrgel napako (FileExistsError), če mapa iz kakršnega koli razloga v tistem trenutku že obstaja.

# 2. Kaj je lahko razlog da mi je python ob zagonu funkcije ki ustvari mapo in potem vanjo dodaja datoteke vrnil to in kaj sploh pomeni zapis z dvojno posevno crto? Namrec vecina linkov je bila take oblike: ime.html, nekateri pa so bili taki chinese/cantonese.htm, torej da so bili pod neko druzino jezikov. Kako to razresim?

FileNotFoundError: [Errno 2] No such file or directory: 'surovi_podatki\\chinese/cantonese.htm'

To je ena izmed najbolj klasičnih pasti pri delu z datotekami v Pythonu! Napaka FileNotFoundError se je zgodila, ker je Python poskusil ustvariti datoteko v mapi, ki sploh še ne obstaja.

Poglejva natančno, kaj se dogaja in kako to elegantno rešiti.

1. Kaj pomeni zapis z dvojno poševnico (\\)?
Dvojna poševnica nazaj (\\) je posebnost operacijskega sistema Windows.

V programiranju poševnica nazaj (\) pomeni t.i. uidejoči znak (escape character), ki napove posebno funkcijo (npr. \n pomeni nova vrstica). Ker Windows uporablja poševnico nazaj za ločevanje map, mora Python (in drugi jeziki) to poševnico podvojiti (\\), da operacijskemu sistemu pove: "To je navadna poševnica za mapo, ne pa začetek posebnega ukaza."

V čem je težava pri tebi?
Tvoja pot izgleda takole: 'surovi_podatki\\chinese/cantonese.htm'

surovi_podatki\\ -> Windows stil (Python je to dodal samodejno za glavno mapo).

chinese/cantonese.htm -> Spletni stil (t.i. forward slash /), ki si ga dobil iz povezave.

Ko se ti dve stvari združita, Python išče mapo chinese znotraj mape surovi_podatki. Ker pa si ti z ukazom mkdir() verjetno ustvaril le mapo surovi_podatki, podmape chinese pa nisi, ti Python javi napako: "No such file or directory". Python namreč zna samodejno ustvariti datoteko, ne zna pa samodejno ustvariti map, ki vodijo do nje.

2. Kako to rešiti?
Najboljša in najvarnejša rešitev je ponovno uporaba knjižnice pathlib, ki jo že poznava. Ta knjižnica ima genialno lastnost: sama popravi mešane poševnice (/ in \) glede na to, ali uporabljaš Windows, Mac ali Linux, poleg tega pa lahko z njo ustvariš vse manjkajoče podmape tik pred pisanjem datoteke.

Tukaj je primer, kako popraviti tvojo kodo:

Python
from pathlib import Path

def shrani_datoteko(glavna_mapa: str, podpot_iz_linka: str, vsebina: str):
    # 1. Združimo glavno mapo in pot iz linka v en varen objekt Path
    # Path bo samodejno popravil 'chinese/cantonese.htm' v pravilen format za tvoj OS
    polna_pot = Path(glavna_mapa) / podpot_iz_linka
    
    # polna_pot sedaj izgleda nekako tako: surovi_podatki/chinese/cantonese.htm
    
    # 2. Poiščemo mapo, v kateri bi morala biti ta datoteka (torej: surovi_podatki/chinese)
    mapa_za_ustvarit = polna_pot.parent
    
    # 3. Ustvarimo to mapo in VSE njene nadrejene mape, če še ne obstajajo
    # parents=True je ključen: ustvaril bo tako 'surovi_podatki' kot 'chinese'
    mapa_za_ustvarit.mkdir(parents=True, exist_ok=True)
    
    # 4. Sedaj varno zapišemo datoteko, saj mapa zagotovo obstaja
    with open(polna_pot, "w", encoding="utf-8") as f:
        f.write(vsebina)
        
    print(f"Datoteka uspešno shranjena na: {polna_pot}")

## Primer uporabe:
shrani_datoteko("surovi_podatki", "chinese/cantonese.htm", "<html>Kantonščina</html>")
shrani_datoteko("surovi_podatki", "ime.html", "<html>Navadna stran</html>")
Kaj se je spremenilo?
Zahvaljujoč polna_pot.parent in mkdir(parents=True, exist_ok=True) program sedaj deluje takole:

Vzame surovi_podatki/ime.html -> pogleda starša (surovi_podatki), ga ustvari (če ga še ni) in shrani datoteko.

Vzame surovi_podatki/chinese/cantonese.htm -> pogleda starša (surovi_podatki/chinese), ustvari celotno to pot (torej tudi mapo chinese) in nato brez težav shrani datoteko.

# 3. Ali je smiselno da se mapo kjer je na tisoce spletnih strani, dati v gitignore, saj mi pri source control zdaj kaze 2.3k+ in ne vem ce se sploh da na github naloziti toliko datotek.

Da, več kot smiselno je! Pravzaprav je to najboljša praksa (best practice) v programiranju.

Te tisoče datotek, ki si jih prenesel s spleta, imenujemo surovi podatki (raw data) ali generirana vsebina. Git in GitHub nista namenjena shranjevanju tolikšne količine posameznih datotek s podatki, temveč shranjevanju tvoje programske kode, ki te podatke obdeluje.

Tukaj je razlaga, zakaj je to nujno in kako to urediš v minuti.

Zakaj teh datotek NE želiš v Gitu?
GitHub ima omejitve: GitHub bo začel protestirati ali pa bo postal izjemno počasen, če boš poskusil naenkrat naložiti na tisoče majhnih datotek. Brez težav sprejme velike datoteke (do 100 MB), prenos tisočih majhnih datotek (kot je 2.3k HTML strani) pa lahko popolnoma zablokira Git.

Preglednost kode (Source Control): Trenutno med tistimi 2300 spremembami sploh ne moreš videti svoje Python kode, ki si jo dejansko napisal ali spremenil. Izgubil si pregled nad projektom.

Smisel Gita: Če boš jutri funkcijo zagnal znova in bo Python spet prenesel te strani, bo Git videl 2300 "novih" sprememb, čeprav je koda ostala ista. To uniči zgodovino projekta.

Kako to takoj rešiš?
V korenu svojega projekta (tam, gde imaš glavno Python skripto) ustvari datoteko z imenom .gitignore (pazi na piko na začetku in brez končnic kot je .txt).

V to datoteko preprosto vpiši ime svoje mape, kjer imaš shranjene te spletne strani.

Če se tvoja mapa imenuje surovi_podatki, v .gitignore vpiši:

Plaintext
surovi_podatki/
Ko to datoteko shraniš, bo številka v Source Controlu v tvojem urejevalniku (npr. VS Code) v sekundi padla iz 2300+ nazaj na le nekaj datotek (tvoja koda in .gitignore).

Kaj pa, če kdor koli drug (ali ti na drugem računalniku) potrebuje te podatke?
Standardna praksa v svetu podatkovne analize in programiranja je naslednja:

V kodi pustiš funkcijo (npr. prenesi_podatke()), ki te strani prenese s spleta.

V datoteko README.md napišeš: "Ko prvič zaženete projekt, poženite skripto, da se ustvari mapa surovi_podatki."

Na ta način tvoj GitHub repozitorij ostane lahek (le nekaj kilobajtov), čist in profesionalen.
