import logging




COOKIE_DOMAIN = { # Domene for cookies. Skje
    "postnord": "my.postnord.no",
    "posten": "id.posten.no"
}


SENSOR_PREFIX = "Postsporer "
CONF_ID = "id"
CONF_UPDATE_FREQUENCY = "update_frequency"
CONF_COOKIE_POSTNORD = "cookie_postnord"
CONF_COOKIE_POSTEN = "cookie_posten"

ATTR_LAST_UPDATE = "last_update"
ATTR_ANTALL_PAKKER = "antall_pakker"
ATTR_ANKOMSTDATO = "ankomstdato"
ATTR_SENDER = 'sender'
ATTR_SISTE_OPPDATERING = 'siste_oppdatering'

ATTR_LIST = [


    ATTR_ANKOMSTDATO,
    ATTR_SENDER,
    ATTR_SISTE_OPPDATERING,
    ]

API_ENDPOINT_POSTNORD = "https://my.postnord.no/api/"

_LOGGER = logging.getLogger(__name__)
