import requests, json

class postenPakke:
    def __init__(self,mobilNr,passord):
        self.r = requests.Session()
        self.body = json.dumps({
        "phoneNumber": "+47" + str(mobilNr),
        "password": str(passord) 
    })
        self.headers = {
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
        'Content-Type': 'application/json'
    }
    def set_headers(self,csrfToken):
        self.headers['X-CSRF-Token'] = csrfToken

    def get_csrfToken(self,response :requests.Response):
        for line in response.iter_lines(79,decode_unicode=True):
            if "csrfToken" in str(line):
                csrfToken = line.replace("window.csrfToken =","").strip()[1:-2]
        return csrfToken

    def authenticate_and_get(self):
        url = "https://id.posten.no/minside" # Første runde henter csrf-token
        with self.r.get(url=url, headers=self.headers) as response:
            csrfToken = self.get_csrfToken(response)
            self.set_headers(csrfToken)
            url = "https://id.posten.no/api/session" # Andre runde gjør innloggingen
            self.r.post(url=url,headers=self.headers,data=self.body)
            url = "https://id.posten.no/minside" # Tredje runde gjør OAuth-autentiseringa
            j = self.r.get(url=url,headers=self.headers)
            url = "https://id.posten.no/user/api/sporing"
            content = self.r.get(url=url,headers=self.headers)
            return content.json()




if "__main__" == __name__:
    posten = postenPakke("98432288","LampeBord99")
    content = posten.authenticate_and_get()
    print(content)