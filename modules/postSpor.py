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

from modules.postnord import postnordManager
from modules.vars import *
from modules.posten import postenPakke
import requests
import appdaemon.plugins.hass.hassapi as hass

class pakkeSpor(hass.Hass):
    def __init__(self, run = False,postenCredentials=None,postnordSecret = None):
        self.data = None
        self.postenCredentials = postenCredentials
        self.postnordSecret = postnordSecret
        self.combiner()

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
        if post_tjeneste == POSTNORD:
            postNord = postnordManager(self.postnordSecret)
            response = postNord.main()
            try: 
                pakker = response[TO]; antall = len(pakker)
            except Exception as e:
                print("postSpor.py, inside fetchShipment()",e)
                return None
        elif post_tjeneste == POSTEN:
            pp = postenPakke(*self.postenCredentials).authenticate_and_get()
            pakker =pp[(ARCHIVED if not RECEIVING else RECEIVE)]
            antall = len(pakker)
        return antall, pakker

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
