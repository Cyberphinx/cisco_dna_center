import requests
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC_IP, DNAC_PORT, DNAC_USER, DNAC_PASSWORD


def get_device_list():
    """
    Building out function to retrieve list of devices.
    Using requests.get to make a call
    """
    token = get_auth_token()  # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    # Make the Get Request
    response = requests.get(url, headers=hdr, verify=False)
    device_list = response.json()
    print_device_list(device_list)


def print_device_list(device_json):
    """
    Apply a filter to the data and look for a specific device by creating a
    query string variable queryString and passing the variable part of the
    param parameter in your requests.get call.
    """
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format(
              "hostname", "mgmt IP", "serial", "platformId", "SW Version",
              "role", "Uptime")
          )
    for device in device_json['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(
                ","), device['platformId'].split(","))
        else:
            serialPlatformList = [
                (device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'], uptime))


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call
    to the Auth Endpoint
    """
    # Endpoint URL
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'
    resp = requests.post(url, auth=HTTPBasicAuth(
        DNAC_USER, DNAC_PASSWORD), verify=False)  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token
    return token    # Create a return statement for the Token


if __name__ == "__main__":
    get_device_list()
