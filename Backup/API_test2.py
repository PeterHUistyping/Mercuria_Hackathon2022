import requests
import base64

user = '6Cheese'
token = 'Token ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c'
url = 'https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2022-08-01&end_date=2022-08-02'

auth = user + ":" + token
encoded = base64.b64encode(bytes(auth, "utf-8"))
encodedAuth = encoded.decode("utf-8")

headers = {
  "Accept":"application/json",
  "Content-Type":"application/json",
  "Authorization":"Bearer " + encodedAuth
}

r = requests.get(url, headers=headers)
print(r)