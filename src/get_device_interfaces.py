import requests
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC_IP, DNAC_PASSWORD, DNAC_PORT, DNAC_USER


def get_device_list():
    """
    Building out function to retrieve list of device.
    Using requests.get to make a call to the network device Endpoint
    """
    global token
    # Get Token
    token = get_auth_token()
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    # Make the Get Request
    resp = requests.get(url, headers=hdr, verify=False)
    device_list = resp.json()
    get_device_id(device_list)


def get_device_id(device_json):
    """
    Get the deviceId you need to send to retrieve the interface. You loop
    through the list in the response.
    """
    for device in device_json['response']:
        print(
            "Fetching Interfaces for Device Id ----> {}".format(device['id']))
        print('\n')
        get_device_int(device['id'])
        print('\n')


def get_device_int(device_id):
    """
    Building out function to retrieve device interface. Using requests.get
    to make a call to the network device Endpoint
    """
    url = "https://sandboxdnac.cisco.com/api/v1/interface"
    hdr = {'x-auth-token': token, 'content-type': 'application/json'}
    querystring = {"macAddress": device_id}
    resp = requests.get(url, headers=hdr, params=querystring, verify=False)
    interface_info_json = resp.json()
    print_interface_info(interface_info_json)


def get_auth_token():
    """
    Building out Auth request.
    Using requests.post to make a call to the Auth Endpoint
    """
    # Endpoint URL
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'
    # Make the POST Request
    resp = requests.post(url, auth=HTTPBasicAuth(
        DNAC_USER, DNAC_PASSWORD), verify=False)
    # Retrieve the Token
    token = resp.json()['Token']
    # Create a return statement for the Token
    return token


def print_interface_info(interface_info):
    """
    Here you want to make the printed output easy to read.
    """
    print("{0:42}{1:17}{2:12}{3:18}{4:17}{5:10}{6:15}".
          format(
              "portName", "vlanId", "portMode", "portType",
              "duplex", "status", "lastUpdated")
          )
    for int in interface_info['response']:
        print("{0:42}{1:10}{2:12}{3:18}{4:17}{5:10}{6:15}".
              format(str(int['portName']),
                     str(int['vlanId']),
                     str(int['portMode']),
                     str(int['portType']),
                     str(int['duplex']),
                     str(int['status']),
                     str(int['lastUpdated'])))


if __name__ == "__main__":
    get_device_list()
