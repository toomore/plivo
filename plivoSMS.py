# -*- coding: utf-8 -*-
import json
import os
import requests
import setting
from pprint import pprint


class plivo(object):
    def __init__(self, auth_id, auth_token, api_version='v1',
            api_url='https://api.plivo.com/'):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.api_url = os.path.join(api_url, api_version)

    def send_sms(data):
        headers = {'content-type': 'application/json'}
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        result = requests.post(endpoint, data=json.dumps(data), headers=headers,
                               auth=(self.auth_id, self.auth_token))
        return result.json()

if __name__ == '__main__':
    text = u'這是一封測試簡訊 This a test SMS.'*2
    data = {
            'src': setting.msg_from,
            'dst': setting.msg_to,
            'text': text + str(len(text)),
           }
    pprint(send_sms(data))
