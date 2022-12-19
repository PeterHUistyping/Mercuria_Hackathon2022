import requests 
url1 = "https://api.com/api/ais-hourly/?start_date=2022-08-01&end_date=2022-08-02"
headers = {
"Authorization": "Token ",
# "accept" : "application/json",
}
username="6"
password ="R"
resp = requests.get(url1,headers=headers)
if resp.status_code != 200:
    print('error: ' + str(resp.status_code))
else:
    print(resp.text)
