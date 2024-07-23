from dnacentersdk import api
from dnac_config import DNAC_IP, DNAC_PORT, DNAC_USER, DNAC_PASSWORD

dnac_url = f"https://{DNAC_IP}:{DNAC_PORT}"

# The underscore behind the variable name is to escape reserved keyword 'api'
api_ = api.DNACenterAPI(
    username=DNAC_USER,
    password=DNAC_PASSWORD,
    base_url=dnac_url,
    version="2.3.7.6",
    verify=False
)
try:
    devices = api_.devices.get_device_list(family="Switches and Hubs")
    for device in devices.response:
        print('{:20s} {} Ip: {}'.format(device.hostname,
              device.upTime, device.managementIpAddress))
except api.ApiError as e:
    print(e)
