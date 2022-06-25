

#Konfigurerbar
HASSIO = True
DEBUG = True
RECEIVING = True
MAX_PACKAGES = 40
PROJECT_DIR = "/config/appdaemon/apps/homeassistant-postsporer"
#Tilstander og rotnøkler

CARRIERS    =   ["posten", "postnord"]
POSTEN      =   "posten"
POSTNORD    =   "postnord"
ARCHIVED    =   "archived"
RECEIVE    =   "receive"
SHIPMENTS   =   "shipments"
TO         = "to"


keyNames    =   [ # samme rekkefølge som Home Assistant - sjekk postsporer/const/const.py
                    "ankomstdato",
                    "sender",
                    "siste_oppdatering",
                    "antall_pakker"]

ANKOMSTDATO = "Ankomstdato"
SENDER       = "Sender"
SISTE_OPPDATERING = "Siste_oppdatering"
RESPONSE_VARS = {
                    ANKOMSTDATO     :   "Ankomstdato",
                    SENDER          :   "Sender",
                    SISTE_OPPDATERING : "Siste_oppdatering"
}

# Selvlagde variabler med relevant data
ANTALL_PAKKER           =   "antall_pakker"
TOTAL_PAKKER            =   "total_pakker"


# Nøkkelnavn fra API med relevant data
PARTER_POSTNORD         =  "parties"
SENDER_POSTNORD         =  "consignor"
SENDERNAVN_POSTNORD     =  "name"

ANKOMSTDATO_POSTNORD    =   "estimated_delivery_at"
SISTE_OPPDATERING_POSTNORD = "status_text"

ANKOMSTDATO_POSTEN      =   "Ikke tilgjengelig"
SENDER_POSTEN           =   "sendersName"
SISTE_OPPDATERING_POSTEN=   "pickupDescription"



#Requests-relaterte variabler

COOKIE = "Cookie"
POSTEN_URL  =   "https://id.posten.no/user/api/sporing"  # Henta gjennom Postman
POSTNORD_URL=   "https://my.postnord.no/api/shipments/"     # Henta gjennom Postman
COOKIE_DOMAIN=  { # Domene for cookies.
                    "postnord": "my.postnord.no",
                    "posten": "id.posten.no"
                }

#Feilmeldinger
ERROR       =   "An error occured. \n"
TYPE_ERROR  =    " is not configured. Please check your spelling."
VALUE_ERROR =   "Some bad shit just happened"
