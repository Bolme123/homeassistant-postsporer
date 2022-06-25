import requests, json
from .vars import *

class postnordManager:
    cookieFile = PROJECT_DIR+"/.cache/POSTNORD"
    configFile = PROJECT_DIR +"/.cache/conf"
    dumpFile = PROJECT_DIR+"/JSONDUMP"
    def __init__(self,postnordSecret):
        self.postnordSecret = postnordSecret
        
    def isConfigured(self,done = False):
        if done == True:
            with open(self.configFile,"w") as f:
                f.write("true")
        else:
            with open(self.configFile,"r") as f:
                content = f.read()
                if content == "true":
                    return True
                else: return False
            
    def setPostnordCookie(self):
        s = requests.session()
        if self.isConfigured():
            with open(self.cookieFile,"r") as f:
                localCookie = f.read()
        else:
            localCookie = self.postnordSecret
            self.isConfigured(done=True)
        s.cookies.set("laravel_session",localCookie,domain="my.postnord.no")
        return s
    def dumpContents(self,response : requests.Response):
        with open(self.dumpFile,"w") as f:
           f.write(str(response.json()))
        
    def getPostnordData(self,session: requests.Session):
        response = session.get(POSTNORD_URL)
        self.updateSessionCookie(response)
        if response.status_code == 200:
            return response.json()
        else:
            return "Could not retrieve data from server", response
        
    def updateSessionCookie(self,response: requests.Response):
        with open(self.cookieFile,"w") as f:
            f.write(response.cookies.get(name="laravel_session"))
        return
    
    def main(self):
        session = self.setPostnordCookie()
        content = self.getPostnordData(session)
        return content