import requests
from requests.auth import HTTPBasicAuth
import env_lab

requests.packages.urllib3.disable_warnings()


def get_auth_token():
    # Endpoint URL
