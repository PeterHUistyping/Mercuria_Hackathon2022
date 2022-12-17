import requests 
import json
def export_results(dictionary, filename):
    with open(filename, 'w') as json_f:
        export_json = json.dumps(dictionary, indent=4)
        json_f.write(export_json)
def extract_and_export(i,url1):
    # url1 = "https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2021-08-01&end_date=2021-08-02"
    headers = {
    "Authorization": "Token ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c",
    # "accept" : "application/json",
    }
    # username="6Cheese"
    # password ="Rudolph123"
    resp = requests.get(url1,headers=headers)
    if resp.status_code != 200:
        print('error: ' + str(resp.status_code))
    else:
        # print(resp.text)
    #store in the json
        json_resp = resp.json()
        print(json_resp['next'])
        # print(resp['result'])     
        export_results(json_resp["results"],f"json/{i}.json")
        return "http://"+json_resp['next']
count=1
next_url='1'
while next_url!='null':
    print(next_url)
    next_url=extract_and_export(count,url1=f"https://api.hackathon.mercuria-apps.com/api/ais-hourly/?end_date=2022-08-02&page={count}&page_size=1000&start_date=2022-08-01")
    count+=1
# print(resp['results'])
# while resp['next']!='null':
#     resp=extract(resp['next'])

