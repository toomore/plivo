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

    def _requests(self, method, endpoint, data={}, *args, **kwargs):
        requests_with_session = requests.Session()
        requests_with_session.auth = (self.auth_id, self.auth_token)
        requests_with_session.headers = {'content-type': 'application/json',
                                         'Connection': 'Keep-Alive',}
        if method == 'POST':
            return requests_with_session.post(endpoint,
                                              data=json.dumps(data)).json()
        elif method == 'GET':
            return requests_with_session.get(endpoint,
                                             params=json.dumps(data)).json()
        else:
            return {'error': 'No method.'}

    def send_sms(self, data):
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def get_account(self):
        endpoint = os.path.join(self.api_url,
                                'Account/%s' % setting.auth_id)
        result = self._requests('GET', endpoint)
        return result

if __name__ == '__main__':
    from datetime import datetime
    #text = u'這是一封測試簡訊 This a test SMS.'*2
    #data = {
    #        'src': setting.msg_from,
    #        'dst': setting.msg_to,
    #        'text': text + str(len(text)),
    #       }
    plivo_tools = plivo(setting.auth_id, setting.auth_token)
    #pprint(plivo_tools.send_sms(data))
    t1 = datetime.now()
    pprint(plivo_tools.get_account())
    print datetime.now() - t1
    pprint(plivo_tools.get_account())
    print datetime.now() - t1
