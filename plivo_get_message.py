# -*- coding: utf-8 -*-
import requests
import setting
from pprint import pprint

AUTH_ID = setting.auth_id
AUTH_TOKEN = setting.auth_token
PLIVO_MSG_URL = 'https://api.plivo.com/v1/Account/%s/Message/' % AUTH_ID

data = requests.get(PLIVO_MSG_URL, params={'limit': 5},
        auth=(AUTH_ID, AUTH_TOKEN))

pprint(data.json())
