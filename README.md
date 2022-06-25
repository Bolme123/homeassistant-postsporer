# homeassistant-postsporer
### Postsporer for bruk med Appdaemon på Home Assistant
kontaktinfo: [GitHub](https://www.github.com/bolme123)



Postsporer - Laga av mej.
Hente pakka fra Postnord og Posten, og returnere relevant info om pakka på vei.

Laga for bruk med AppDaemon i Home Assistant
Cheers


### Konfigurasjon
  Programmet tar i bruk 2 parameter
  Parameter | Forklaring
------------- | -------------------------
POSTNORD_COOKIE | Session-ID fra innlogget Postnord-økt 
  Du må hent Session-ID for Postnord manuelt.
  
  Deretter, Åpne apps.yaml 
  ##### eksempel apps.yaml
  ```yaml
homeassistant-postsporer:
  module: postsporer
  class: Get_Shit
  POSTEN_CREDENTIALS: 
    - 40294827 # Registrert mobilnr for Posten-konto
    - "Password" # Passord for nevnt konto
  POSTNORD_COOKIE: !secret POSTNORDCOOKIE # Laravel-cookie tilhørende Postnord
  ```
# NOTE
Session ID'en fra PostNord endrer seg kontinuerlig, så etter programmet har 'brukt' cookien oppe så vil programmet videre bruke en cachet fil i /.cache/POSTNORD.
Skulle du trenge å bruke cookien satt i Apps.yaml igjen så gjør du slik
* Gå til /.cache/conf
* Slett alt, skriv deretter false
   

### TO DO
* Lægg t støtte for flere postsporingsystem 
    * DHL
    * DPD
    * AliExpress
    * eBay
    * BangGood
* Automatisere Session-innsamlingen
    * Ved første-konfigurasjon setter man hvilke sporesystem en ønsker, deretter forsøker programmet å logge inn på hver enkelt platform, fanger Session-ID
* Legg til hentekode for Posten


### Bugs
 * Om en endrer leveringsmetode på PostNord midt i sendingen kan det komme to identiske pakker


### Ressurser
 * Home Assistant
 * AppDaemon
 * Postman
 * Posttjeneste-platformer
   * Posten
   * Postnord
