# -*- coding: utf-8 -*-
''' plivo api '''
import os
import requests
import setting
import ujson as json
from pprint import pprint


class Plivo(object):
    ''' plivo API

        :param str auth_id: plivo auth_id
        :param str auth_token: plivo auth_token
        :param str api_version: plivo api version, default 'v1'
        :param str api_url: plivo api url
    '''
    def __init__(self, auth_id, auth_token, api_version='v1',
            api_url='https://api.plivo.com/'):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.api_url = os.path.join(api_url, api_version)

    def _requests(self, method, endpoint, data=None, *args, **kwargs):
        ''' requests wraps '''
        requests_with_session = requests.Session()
        requests_with_session.auth = (self.auth_id, self.auth_token)
        requests_with_session.headers = {'content-type': 'application/json',
                                         'Connection': 'Keep-Alive',}
        data = json.dumps(data)
        if method == 'POST':
            result = requests_with_session.post(endpoint, data=data)
        elif method == 'GET':
            result = requests_with_session.get(endpoint, params=data)
        else:
            return {'error': 'No method.'}

        if result.status_code == requests.codes.ok:
            return json.loads(result.text)
        else:
            return {'error': 'requests error.'}

    def send_sms(self, data):
        ''' Send SMS
            Ref: http://plivo.com/docs/api/message/

            :rtype: dict
        '''
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def make_call(self, data):
        ''' Make a call
            Ref: http://plivo.com/docs/api/call/

            :rtype: dict
        '''
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Call/' % setting.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def get_sms(self, message_uuid=None):
        ''' Get SMS info.
            Ref: http://plivo.com/docs/api/message/

            :rtype: dict
        '''
        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        if message_uuid:
            endpoint = os.path.join(endpoint, message_uuid)

        result = self._requests('GET', endpoint)
        return result

    def get_account(self):
        ''' Get Account info
            Ref: http://plivo.com/docs/api/account/

            :rtype: dict
        '''
        endpoint = os.path.join(self.api_url, 'Account/%s' % setting.auth_id)
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
    plivo_tools = Plivo(setting.auth_id, setting.auth_token)

    # ----- send sms ----- #
    #pprint(plivo_tools.send_sms(data))
    #t1 = datetime.now()
    #pprint(plivo_tools.get_account())
    #print datetime.now() - t1
    #pprint(plivo_tools.get_account())
    #print datetime.now() - t1

    # ----- get sms ----- #
    #pprint(plivo_tools.get_sms())
    #pprint(plivo_tools.get_sms('f12115e4-891b-11e3-944e-1231400195a3'))

    # ----- make call ----- #
    #data = {
    #        'from': setting.msg_from,
    #        'to': setting.msg_to,
    #        'answer_url': 'https://s3.amazonaws.com/plivosamplexml/speak_url.xml',
    #        'answer_method': 'GET',
    #       }
    #make_call = plivo_tools.make_call(data)
    #pprint(make_call) # request_uuid
