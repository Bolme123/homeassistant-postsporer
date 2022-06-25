import requests, json, datetime
import appdaemon.plugins.hass.hassapi as hass
from modules.postSpor import pakkeSpor
import ha_version
from modules.vars import *
class Get_Shit(hass.Hass): # Deklarerer egenskaper for klassen.

    def initialize(self):
        self.log(
            f"🚨 Launching Get_Shit {ha_version.__version__}",
            ascii_encode=False,
        )
        self.POSTEN_COOKIE = self.args["POSTEN_COOKIE"]
        self.POSTNORD_COOKIE = self.args["POSTNORD_COOKIE"]
        self.cookie_dict = {
                            "posten": self.POSTEN_COOKIE,
                            "postnord": self.POSTNORD_COOKIE
        }
        self.data = None
        self.ps = None
        self.total_pakker = None
        self.pakkeliste = None
        
        self.load_sensors()
#        def getData(self,entity, attribute, old, new, kwargs):
        runtime = datetime.time(0, 0, 0)
        self.run_hourly(self.run_hourly_callback, runtime)
        """
        Lag en liste for å  dumpe sensor-navnene fortløpende.
        Sjekk etter navnevalg om nåværende kalkulert navn allerede eksisterer i listen, 
        isåfall legg til et tall i navn og sjekk igjen
        """
        
    def postSensor(self):
        name = ""
        ignoreKeys = ["antall_pakker", "posten", "postnord"]
        sensorNavn = []
        if self.data != None:
            for parcels in self.data:
                if str(parcels) != "total_pakker":
                    if self.data[parcels] != None:
                        for parcel in self.data[parcels]:
                            if str(parcel) not in ignoreKeys:
                                name = str(self.data[parcels][parcel]["Sender"]).replace(" ","_").replace(".","_").replace("-","_").lower()
                                lastchar : str =""
                                length: int = len(name)
                                count = 0
                                while length > count:
                                    if name[count] == name[count-1] and name[count] == "_":
                                        name = name[0:count:] + name[count+2::]
                                    length = len(name)
                                    count += 1
                                while True:
                                    if name in sensorNavn:
                                        name+="n"
                                    else:
                                        sensorNavn.append(name)
                                        break
                                    
                                self.set_state(("sensor.postpakker_" + name),
                                    state = str(self.data[parcels][parcel]["Siste_oppdatering"]),
                                    attributes= {
                                    "info": self.data[parcels][parcel]
                                        }
                                    )
                    else: 
                        pass
        else: 
            pass
        self.set_state("sensor.postpakker",
            state=str(self.total_pakker) + (" pakke på vei" if self.total_pakker == 1 else " pakker på vei"),
            replace = True, attributes= {
            "icon": "mdi:mail",
            "friendly_name": "postsporer",
            "Info": self.data
         })
        return True

    def load_sensors(self): #Kjører ved oppstart
        self.getData()
        self.postSensor()
        
        
    def run_hourly_callback(self, kwargs):
        self.getData()
        try:
            self.postSensor()
        except:
            self.log("Something went terribly wrong.")
            pass

        
    def getData(self):
        self.ps = pakkeSpor(self.cookie_dict)
        self.data = self.ps.data
        self.log(
                f"🚨 data:  "+ str(self.data),
                  ascii_encode=False
         )
        self.total_pakker = self.ps.data[TOTAL_PAKKER]
        return
