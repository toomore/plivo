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

    def _requests(self, method, endpoint, data, *args, **kwargs):
        headers = {'content-type': 'application/json'}
        if method == 'POST':
            return requests.post(endpoint, data=json.dumps(data),
                    headers=headers,
                    auth=(self.auth_id, self.auth_token)).json()
        elif method == 'GET':
            return requests.get(endpoint, params=json.dumps(data),
                    headers=headers,
                    auth=(self.auth_id, self.auth_token)).json()
        else:
            return {'error': 'No method.'}

    def send_sms(self, data):
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

if __name__ == '__main__':
    text = u'這是一封測試簡訊 This a test SMS.'*2
    data = {
            'src': setting.msg_from,
            'dst': setting.msg_to,
            'text': text + str(len(text)),
           }
    plivo_tools = plivo(setting.auth_id, setting.auth_token)
    pprint(plivo_tools.send_sms(data))
