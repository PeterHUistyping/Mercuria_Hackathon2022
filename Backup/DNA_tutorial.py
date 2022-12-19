import requests
from requests.auth import HTTPBasicAuth  # DNA Center uses basic authentication.
import urllib3

# Disable HTTPS insecure certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = "devnetuser"
password = "Cisco123!"

def get_token(username, password):
    """
    Authenticate to DNA Center and get token.
    """
    url = "https://sandboxdnac.cisco.com/api/system/v1/auth/token"

    # API uses JSON.
    headers = {'content-type': 'application/json'}
    # Send HTTP POST with username and password.
    response = requests.request("POST",
                                url, 
                                auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)
    
    # Save the token in a variable.
    token = response.json()["Token"]
    return token


def get_data_from_dna_center(token, endpoint):
    """
    Communicate with DNA Center to retrieve network information.
    """

    # Include the token in the header.
    headers = {'content-type': 'application/json', 'x-auth-token': token}
    # Send HTTP GET to retrieve endpoint.
    response = requests.get('https://sandboxdnac.cisco.com/api/v1/%s' % endpoint, headers=headers, verify=False)
    response_as_dict = response.json() # convert JSON to DICT.
    return response_as_dict

# Run function to authenticate and get token.
token = get_token(username, password)
# Retrieve list with network devices of DNA center.
network_devices_info = get_data_from_dna_center(token, "network-device")

# Print list with network devices.
for device in network_devices_info['response']:
    device_type = device['type']
    uptime = device['upTime']

    print("Device: %s has an uptime of %s." % (device_type, uptime))