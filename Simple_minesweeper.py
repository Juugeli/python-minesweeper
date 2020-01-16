# -*- coding: utf-8 -*-

import random, time

def ota_arvot():
    """
    Ottaa käyttäjältä kentän leveyden, korkeuden ja miinojen lukumäärän.
    Palauttaa kyseiset tiedot tallennettuina muuttujiin.
    """
    while True:
        syote_leveys = raw_input("\nAnna kentän leveys: ")
        if syote_leveys.isdigit():
            leveys = int(syote_leveys)
            if leveys <= 0:
                print "\nLeveyden pitää olla vähintään yksi."
            else:
                break
        else:
            print "\nAnna leveys positiivisena kokonaislukuna."

    while True:
        syote_korkeus = raw_input("\nAnna kentän korkeus: ")
        if syote_korkeus.isdigit():
            korkeus = int(syote_korkeus)
            if korkeus <= 0:
                print "\nKorkeuden pitää olla vähintään yksi."
            else:
                break
        else:
            print "\nAnna korkeus positiivisena kokonaislukuna."

    while True:
        syote_miina_lkm = raw_input("\nMiinojen lukumäärä kentällä: ")
        if syote_miina_lkm.isdigit():
            miina_lkm = int(syote_miina_lkm)
            if miina_lkm <= 0:
                print "\nMiinoja tulee olla vähintään yksi."
            elif miina_lkm > leveys * korkeus:
                print "\nKaikkien miinojen tulee mahtua kentälle."
            else:
                break
        else:
            print "\nAnna miinojen lukumäärä positiivisena kokonaislukuna."

    return leveys, korkeus, miina_lkm



def luo_kentta(leveys, korkeus, miina_lkm):
    """
    Ottaa sisään leveyden, korkeuden ja miinojen lukumäärän.
    Luo tietojen pohjalta oikean kentän, pelaajalle näytettävän kentän ja pelattavat koordinaatit.
    """
    oikea_kentta = []
    pelaajan_kentta = []
    for y in range(korkeus):
        oikea_kentta.append([0] * leveys)
        pelaajan_kentta.append(["?"] * leveys)

    pelattavat_koordinaatit_miinoitus = []
    for x in range(leveys):
        for y in range(korkeus):
            pelattavat_koordinaatit_miinoitus.append((x, y))

    pelattavat_koordinaatit = []
    for x in range(leveys):
        for y in range(korkeus):
            pelattavat_koordinaatit.append((x, y))
    for miina in range(miina_lkm):
        
        while True:
            miinakoordinaatti = random.choice(pelattavat_koordinaatit_miinoitus)
            y = miinakoordinaatti[1]
            x = miinakoordinaatti[0]
            if oikea_kentta[y][x] == "x":
                continue
            else:
                oikea_kentta[y][x] = "x"
                pelattavat_koordinaatit_miinoitus.remove(miinakoordinaatti)
                break

    return oikea_kentta, pelaajan_kentta, pelattavat_koordinaatit

def laske_miinat(xkoord, ykoord, huone):
    """
	Laskee yhden ruudun ympäröivät miinat.
	"""
    miinalista = []
    for rivi in huone[max((ykoord - 1), 0) : min((ykoord + 2), len(huone))]:
        for x in rivi[max((xkoord - 1), 0) : min((xkoord + 2), len(huone[0]))]:
            if x == "x":
                miinalista.append("m")
    summa = len(miinalista)
    return summa

def valmista_kentta(oikea_kentta):
    """
    Laskee jokaiseen miinattomaan ruutuun ympäröivien miinojen määrän.
    """
    for rivi in range(len(oikea_kentta)):
        for alkio in range(len(oikea_kentta[0])):
            if oikea_kentta[rivi][alkio] == 0:
                miinat = laske_miinat(alkio, rivi, oikea_kentta)
                oikea_kentta[rivi][alkio] = miinat
    return oikea_kentta

def anna_koordinaatit(oikea_kentta):
    """
    Ottaa pelaajalta pelattavat koordinaatit ja tarkistaa, että ne osuvat kentän sisälle.
    Palauttaa pelatut koordinaatit.
    """
    while True:
        x_koord = raw_input("Anna x-koordinaatti väliltä 0 - %s: " % (len(oikea_kentta[0]) - 1))
        if x_koord.isdigit():
            x_koord = int(x_koord)
            if 0 <= x_koord <= len(oikea_kentta[0]) - 1:
                break
            else:
                print "Koordinaattisi meni kentän ulkopuolelle."
        else:
            print "Anna positiivinen kokonaisluku."

    while True:
        y_koord = raw_input("Anna y-koordinaatti väliltä 0 - %s: " % (len(oikea_kentta) - 1))
        if y_koord.isdigit():
            y_koord = int(y_koord)
            if 0 <= y_koord <= len(oikea_kentta) - 1:
                break
            else:
                print "Koordinaattisi meni kentän ulkopuolelle."
        else:
            print "Anna positiivinen kokonaisluku."

    return x_koord, y_koord

def tulvataytto(oikea_kentta, pelaajan_kentta, x, y, pelattavat_koordinaatit):
    """
    Alkaa avaamaan annetusta koordinaatista alkaen aluetta, kunnes vastaan tulee nollasta poikkeava arvo, miina tai reuna.
    """
    lista = [(x,y)]
    while len(lista) > 0:
        koord = lista[-1]
        korkeus = koord[1]
        leveys = koord[0]
        pelaajan_kentta[korkeus][leveys] = str(oikea_kentta[korkeus][leveys])
        if (leveys, korkeus) in pelattavat_koordinaatit:
            if oikea_kentta[korkeus][leveys] == 0:

                if oikea_kentta[max((korkeus - 1), 0)][leveys] >= 0:
                    lista.append((leveys, max((korkeus - 1), 0)))

                if oikea_kentta[min((korkeus + 1), (len(oikea_kentta) - 1))][leveys] >= 0:
                    lista.append((leveys, min((korkeus + 1), (len(oikea_kentta) - 1))))

                if oikea_kentta[korkeus][max((leveys - 1), 0)] >= 0:
                    lista.append((max((leveys - 1), 0), korkeus))

                if oikea_kentta[korkeus][min((leveys + 1), (len(oikea_kentta[0]) - 1))] >= 0:
                    lista.append((min(leveys + 1, len(oikea_kentta[0]) - 1), korkeus))

                lista.remove(koord)
                pelattavat_koordinaatit.remove((leveys, korkeus))
            elif oikea_kentta[korkeus][leveys] > 0:
                lista.remove(koord)
                pelattavat_koordinaatit.remove((leveys, korkeus))
        else:
            lista.remove(koord)

def tilaston_tallennus(pvm, kesto, vuorot, tulos, leveys, korkeus, miina_lkm):
    """
    Ottaa pelatun pelin tiedot, luo niistä yhden merkkijonon ja tallentaa sen tiedostoon.
    """
    tilastot = open("miinaharavan_tilasto.txt", "a")
    kesto = "%s min %s s" % ((kesto / 60), (kesto % 60))
    pelin_tiedot = "\nPäivämäärä: %s\nPelin kesto: %s\nVuorojen lukumäärä: %s\nTulos: %s\nPelikentän leveys: %s\nPelikentän korkeus: %s\nMiinojen lukumäärä: %s\n" % (pvm, kesto, vuorot, tulos, leveys, korkeus, miina_lkm)
    tilastot.write(pelin_tiedot)
    tilastot.close()
    
def tilaston_luku():
    """
    Lukee tiedostosta tilastotiedot ja tulostaa ne käyttäjälle.
    Jos tiedostoa ei ole olemassa, kertoo tämän käyttäjälle.
    """
    try:
        tilastot = open("miinaharavan_tilasto.txt")
        print "\nTilastot:"
        print tilastot.read()
        tilastot.close()
    except IOError, NameError:
        print "\nTilastoja ei ole vielä olemassa!"
    
if __name__ == "__main__":
    print "\n\n# Tervetuloa miinantallaaja-peliin! #\n"
    while True:
        try:
            valinta = raw_input("_____________\n\nPäävalikko:\n\nA) Uusi peli\nB) Tilastot\nC) Lopeta\n_____________\n\nMitä haluat tehdä?: ").lower()
        except EOFError:
            print "\nPakotit pelin lopettamisen."
            exit()
        if valinta == "a":
            print "\nUusi peli valittu!"
            leveys, korkeus, miina_lkm = ota_arvot()
            kesken_kentta, pelaajan_kentta, pelattavat_koordinaatit = luo_kentta(leveys, korkeus, miina_lkm)
            oikea_kentta = valmista_kentta(kesken_kentta)
            vuorot = []
            pvm = time.ctime()
            alkuaika = time.time()
            while True:
                vuorot.append(1)
                print
                for rivi in pelaajan_kentta:
                    print "".join(rivi)
                print
                x_koord, y_koord = anna_koordinaatit(oikea_kentta)
                if len(pelattavat_koordinaatit) >= miina_lkm:
                    if (x_koord, y_koord) in pelattavat_koordinaatit:
                        if oikea_kentta[y_koord][x_koord] == "x":
                            tulvataytto(oikea_kentta, pelaajan_kentta, x_koord, y_koord, pelattavat_koordinaatit)
                            print
                            for rivi in pelaajan_kentta:
                                print "".join("".join(rivi).replace("x", "X"))
                            print "\nOsuit miinaan, hävisit pelin!"
                            tilaston_tallennus(pvm, int(round(time.time() - alkuaika)), len(vuorot), "Häviö", leveys, korkeus, miina_lkm)
                            break
                        else:
                            tulvataytto(oikea_kentta, pelaajan_kentta, x_koord, y_koord, pelattavat_koordinaatit)
                            if len(pelattavat_koordinaatit) == miina_lkm:
                                print
                                for rivi in pelaajan_kentta:
                                    print "".join("".join(rivi).replace("?", "X"))
                                print "\nVoitit pelin!"
                                tilaston_tallennus(pvm, int(round(time.time() - alkuaika)), len(vuorot), "Voitto", leveys, korkeus, miina_lkm)
                                break
                    else:
                        print "\nOlet pelannut kyseisen koordinaatin tai se on jo paljastettu."
        elif valinta == "b":
            tilaston_luku()
        elif valinta == "c":
            print "\nLopetit pelin."
            exit()
        else:
            print "\nValitse jokin vaihtoehdoista A, B tai C!"
