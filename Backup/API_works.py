import requests 
url1 = "https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2022-08-01&end_date=2022-08-02"
headers = {
"Authorization": "Token ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c",
# "accept" : "application/json",
}
username="6Cheese"
password ="Rudolph123"
resp = requests.get(url1,headers=headers)
if resp.status_code != 200:
    print('error: ' + str(resp.status_code))
else:
    print(resp.text)
