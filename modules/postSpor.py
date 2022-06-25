"""
Laga for personlig bruk t Home Assistant

kontaktinfo:
    https://github.com/Bolme123/

Postsporer - Laga av mej.
Hente pakka fra Postnord og Posten, og returnerer relevant info om pakka på vei.
Må hent Session-ID fra både Postnord og Posten manuelt. (Postman funke fjell t d)
Cheers

Om du hente session-ID gjennom Postman så kan du enkelt copy-paste me cookieParse()
    1. fang HTTP-forespørseln med Session-ID.
    2. Klikk på "code" i øvre høyre hjørne.
    3. Velg "Python - Requests" fra dropdown-menyen
    4. i Headers-ordboka, kopier alt fra og med "Cookie" helt ned t klemmeparantesen
    5. deklarer en dict å lim inn.
        Eks:
        eksempel = {
        'Cookie': 'Cookienavn=cookieverdi;cookienavn1=cookieverdi1'
        }

    6. bruk som parameter t første t cookieParse()
    6. andre parameter = domene
    7. profit

domene for postnord-cookies: my.postnord.no
domene for posten-cookies:  id.posten.no

TO DO
    - Lægg t støtte for flere postsporingsystem (DHL, DPD etc)




"""

from threading import local

from matplotlib.pyplot import get
from modules.vars import *
from modules.posten import postenPakke
if not HASSIO: 
    import traceback, sys 
else: 
    pass
import requests
import appdaemon.plugins.hass.hassapi as hass

class pakkeSpor(hass.Hass):
    def __init__(self,cookie_dict, run = False):
        self.cookie_dict = cookie_dict
        self.data = None
        self.combiner()

    def cookieParse(self,cookie, cookiedomain, session: requests.Session ,post_tjeneste):
        if not HASSIO:
            dump = cookie[COOKIE].split(";")
        # print(dump)
        else:
            dump = cookie.split(";")
        if post_tjeneste == POSTEN:
            for k in dump:
                # Deler opp listen nok en gang etter første =-tegn
                split = k.strip(" ").split("=", maxsplit=1)

                cookiename, cookievalue = split[0], split[1]
                session.cookies.set(cookiename,
                                    cookievalue,
                                    domain=cookiedomain)  # Setter cookies. Skal være Session-ID fra en pålogga session.
        elif post_tjeneste == POSTNORD:
            with open(PROJECT_DIR+"/const/POSTNORD","r") as f:
                localCookie = f.read()
                session.cookies.set("laravel_session",localCookie,domain="my.postnord.no")

    def combiner(self):  # Kombinerer pakkene fra postnord og posten

        motherload = {}
        total_pakker = 0
        combolist = []
        for carrier in CARRIERS:
            try:
                motherload[carrier] = self.parseShipment(carrier)
                total_pakker = motherload[carrier][ANTALL_PAKKER] + total_pakker

            except Exception as e:
                print(e)
                continue
        motherload[TOTAL_PAKKER] = total_pakker
        if self.data:
            self.data.clear()
            self.data = motherload #eturnerer
        else:
            self.data = motherload


    def fetchShipment(self,post_tjeneste):
        def getCredentials():
            with open(f"{PROJECT_DIR}/const/CREDENTIAL","r") as f:
                return f.read().split("\n")
            
        s = requests.session()
        if not HASSIO:
            sCookie = self.cookie_dict[post_tjeneste][COOKIE]
        else:
            sCookie = self.cookie_dict[post_tjeneste]
            
        self.cookieParse(
            self.cookie_dict[post_tjeneste], COOKIE_DOMAIN[post_tjeneste], s,post_tjeneste
        )
        if post_tjeneste != POSTEN:
      #  r = s.get((POSTEN_URL if post_tjeneste == POSTEN else POSTNORD_URL))
            r = s.get(POSTNORD_URL)
            with open(f"{PROJECT_DIR}/const/POSTNORD","w") as f:
                f.write(r.cookies.get(name="laravel_session"))
            with open(f"{PROJECT_DIR}/JSONDUMP","w") as f:
                f.write(str(r.json()))
            response = r.json()
        else: 
            response = True

        if not response:  # Hvis det ikke er noe å hente, ferdig. sender 0 til å behandle i update-objektet
            return None
        else:
            # antall indekser i response tilsvarer antall pakker på vei
            if post_tjeneste == POSTNORD:
                root = response[TO]; antall = len(root)
                return antall,root
            else:
                creds = getCredentials()
                root = postenPakke(creds[0],creds[1]).hentaData[(ARCHIVED if not RECEIVING else RECEIVE)]; antall = len(root)
                return antall, root

    def parseShipment(self,carrier):  # Returnerer sender, siste_oppdatering, ankomstdato, antall pakker
        # Lokale variabla for å lagre forskjellig shit
        antall_pakker = 0
        sender = []
        siste_oppdatering = []
        ankomstdato = []  # Bare postnord
        antall_pakker, fetchedPackages = self.fetchShipment(carrier)
        if not antall_pakker:  # Stopp om ingen pakker
            return None
            # Failsafe ferdig
        else:
            try:
                packages = {}
                for pakke in fetchedPackages:
                    x = int(fetchedPackages.index(pakke))
                    root = fetchedPackages[x]
            #        print([pakke])
                    packages[carrier + " " + str(x + 1)] = {
                        RESPONSE_VARS[ANKOMSTDATO]: (ANKOMSTDATO_POSTEN if carrier == POSTEN else root[ANKOMSTDATO_POSTNORD]),
                        RESPONSE_VARS[SENDER]: (root[SENDER_POSTEN] if carrier == POSTEN else root[SENDER_POSTNORD]),
                        RESPONSE_VARS[SISTE_OPPDATERING]: (root[SISTE_OPPDATERING_POSTEN] if carrier == POSTEN else root[SISTE_OPPDATERING_POSTNORD])
                    }
                packages[ANTALL_PAKKER] = antall_pakker
                if carrier == POSTNORD:
                    print(f"DEBUG PACKAGE: {packages}")
                if HASSIO:
                    #_LOGGER.debug("Returning " +carrier +  " data")
                    pass
                else:
                    pass
                return packages
            except Exception as e:
                print(e.with_traceback())
                print(e)
