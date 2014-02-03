# -*- coding: utf-8 -*-
''' plivo api '''
import os
import requests
import setting
import ujson as json


class Plivo(object):
    ''' plivo API

        :param str auth_id: plivo auth_id
        :param str auth_token: plivo auth_token
        :param str api_version: plivo api version, default 'v1'
        :param str api_url: plivo api url
    '''
    def __init__(self, auth_id, auth_token, api_version='v1',
            api_url='https://api.plivo.com/', to_number=None):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.api_url = os.path.join(api_url, api_version)
        if to_number:
            assert isinstance(to_number, str)
            to_number = to_number.strip()
        self.to_number = to_number

    def __repr__(self):
        return 'Plivo api_url: %s, to_number: %s' % (
                self.api_url, self.to_number)

    def _requests(self, method, endpoint, data=None):
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

        #if result.status_code == requests.codes.ok:
        #    return json.loads(result.text)
        #else:
        #    return {'error': 'requests error.',
        #            'result': json.loads(result.text),
        #            'code': result.status_code}
            return json.loads(result.text)

    def send_sms(self, data):
        ''' Send SMS
            Ref: http://plivo.com/docs/api/message/

            :rtype: dict
        '''
        if 'dst' not in data:
            data['dst'] = self.to_number

        endpoint = os.path.join(self.api_url,
                                'Account/%s/Message/' % setting.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def make_call(self, data):
        ''' Make a call
            Ref: http://plivo.com/docs/api/call/

            :rtype: dict
        '''
        if 'to' not in data:
            data['to'] = self.to_number

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
    #from datetime import datetime
    #from pprint import pprint
    #text = u'這是一封測試簡訊 This a test SMS.'*2
    #data = {
    #        'src': setting.msg_from,
    #        'dst': setting.msg_to,
    #        'text': text + str(len(text)),
    #       }
    PILVO_TOOLS = Plivo(setting.auth_id, setting.auth_token,
            to_number=setting.msg_to)

    print PILVO_TOOLS

    # ----- send sms ----- #
    #pprint(PILVO_TOOLS.send_sms(data))

    # ----- Get Account info ----- #
    #t1 = datetime.now()
    #pprint(PILVO_TOOLS.get_account())
    #print datetime.now() - t1
    #pprint(PILVO_TOOLS.get_account())
    #print datetime.now() - t1

    # ----- get sms ----- #
    #pprint(PILVO_TOOLS.get_sms())
    #pprint(PILVO_TOOLS.get_sms('f12115e4-891b-11e3-944e-1231400195a3'))

    # ----- make call ----- #
    #data = {
    #    'from': setting.msg_from,
    #    'to': setting.msg_to,
    #   }
    #make_call = PILVO_TOOLS.make_call(data)
    #pprint(make_call) # request_uuid
