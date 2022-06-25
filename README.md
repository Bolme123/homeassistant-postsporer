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
POSTEN_COOKIE | Session-ID fra innlogget Posten-økt
POSTNORD_COOKIE | Session-ID fra innlogget Postnord-økt
 

  
  Du må hent Session-ID manuelt. (Postman funke fjell t d)
  
  Cookies kan legges inn i apps.yaml i appdaemon/apps.
  
  Om du har satt opp Postman vil æ anbefal å bruk det t å hent session-ID
  
  ##### Hent session-ID gjennom Postman
  1. fang HTTP-forespørseln der du logge inn på Posten/Postnord
      * Pass på at "Capture Cookies" e valgt
  3. Klikk på "code" i øvre høyre hjørne i Postman.
  4. Velg "Python - Requests" fra dropdown-menyen
  5. i Headers-ordboka, kopier alt fra og med "Cookie" helt ned t klemmeparantesen

  Deretter, Åpne apps.yaml 
  ##### eksempel apps.yaml
  ```yaml
  homeassistant-postsporer:
    module: postsporer
    class: Get_Shit
    POSTEN_COOKIE: ''
    POSTNORD_COOKIE: "laravel_session="
  ```


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
 * Session-ID fra posten trenger å fornyes for ofte for å være praktisk 
 * Om en endrer leveringsmetode på PostNord midt i sendingen kan det komme to identiske pakker


### Ressurser
 * Home Assistant
 * AppDaemon
 * Postman
 * Posttjeneste-platformer
   * Posten
   * Postnord
