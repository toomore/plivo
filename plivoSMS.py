# -*- coding: utf-8 -*-
import json
import requests
import setting
from pprint import pprint


def send_sms(data):
    headers = {'content-type': 'application/json'}
    endpoint = 'https://api.plivo.com/v1/Account/%s/Message/' % setting.auth_id
    result = requests.post(endpoint, data=json.dumps(data), headers=headers,
                           auth=(setting.auth_id, setting.auth_token))
    return result.json()

if __name__ == '__main__':
    text = u'這是一封測試簡訊 This a test SMS.'*2
    data = {
            'src': setting.msg_from,
            'dst': setting.msg_to,
            'text': text + str(len(text)),
           }
    pprint(send_sms(data))
