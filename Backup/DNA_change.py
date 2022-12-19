# import requests
# # pip install requests
# from bs4 import BeautifulSoup
# # Beautiful Soup(bs4) is a Python library for pulling data out of HTML and XML files. 
# url_origin='https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2021-04-01&end_date=2021-04-30'
# response=requests.get(url_origin)
# print(response.text)
#
# import requests
# import os
# # Get the API token from an environment variable
# token = 'ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c'
# # Add the Authorization header
# headers = {'Authorization': f'Token {token}'}
# # This is the base URL for all Nautobot API calls
# base_url = 'https://api.hackathon.mercuria-apps.com/api'
# # Get the list of devices from Nautobot using the requests module and passing in the authorization header defined above
# response = requests.get('https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date=2021-04-01&end_date=2021-04-30', headers=headers)
# response.json()
import requests
from requests.auth import HTTPBasicAuth  # DNA Center uses basic authentication.
import urllib3

# Disable HTTPS insecure certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = "6"
password = "R"

# def get_token(username, password):
#     """
#     Authenticate to DNA Center and get token.
#     """
#     url = "https://sandboxdnac.cisco.com/api/system/v1/auth/token"

#     # API uses JSON.
#     headers = {'content-type': 'application/json'}
#     # Send HTTP POST with username and password.
#     response = requests.request("POST",
#                                 url, 
#                                 auth=HTTPBasicAuth(username, password),
#                                 headers=headers, verify=False)
    
#     # Save the token in a variable.
#     token = response.json()["Token"]
#     return token


def get_data_from_dna_center(token):
    """
    Communicate with DNA Center to retrieve network information.
    """

    # Include the token in the header.
    headers = {'content-type': 'application/json', 'x-auth-token': token}
    # Send HTTP GET to retrieve endpoint.
    response = requests.get('https://api.com/api/ais-hourly/?start_date=2022-08-01&end_date=2022-08-30', headers=headers, verify=False)
    response_as_dict = response.json() # convert JSON to DICT.
    return response_as_dict

# Run function to authenticate and get token.
#token = get_token(username, password)
token="ac9ed6b82c1f8c63d728333ae37bba249d2cbb4c"
# Retrieve list with network devices of DNA center.
network_devices_info = get_data_from_dna_center(token)

print(network_devices_info)
# # Print list with network devices.
# for device in network_devices_info['response']:
#     device_type = device['type']
# #     uptime = device['upTime']

#     print("Device: %s has an uptime of %s." % (device_type, uptime))