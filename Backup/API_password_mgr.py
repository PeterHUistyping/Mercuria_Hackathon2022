from urllib.parse import urlparse
from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
import requests
# pip install requests
# url_origin='https://google.com'
url_origin='https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2022-08-01&end_date=2022-08-02'
response=requests.get(url_origin)
password_mgr=HTTPPasswordMgrWithDefaultRealm()
username="6Cheese"
password ="Rudolph123"
Auth = "ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c"
top_level_url = urlparse(url_origin).netloc
print(top_level_url)
password_mgr.add_password(None, top_level_url, username, password)
payload = {'name': 'Peter', 'age': 23}
requests.get(
  url_origin, 
  # password_mgr,
  auth=(username,password)
)
print(response.text)

# curl -X POST -d "{"username":"6Cheese","password":""}" http://localhost:8000/rest-auth/login/ -v