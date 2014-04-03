# -*- coding: utf-8 -*-
''' plivo api '''
import os
import requests
import ujson as json
from collections import Iterable
from collections import deque
from urlparse import urljoin


class Plivo(object):
    ''' plivo API

        :param str auth_id: plivo auth_id
        :param str auth_token: plivo auth_token
        :param str api_version: plivo api version, default 'v1'
        :param str api_url: plivo api url
        :param str to_number: default to number
        :param iter source: default from number
    '''
    def __init__(self, auth_id, auth_token, api_version='v1',
            api_url='https://api.plivo.com/', to_number=None, source=None):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.api_url = urljoin(api_url, '%s/' % api_version)
        if to_number:
            assert isinstance(to_number, basestring)
            to_number = self.format_number(to_number)
        if source:
            if isinstance(source, basestring):
                source = self.format_number(source)
                self._numbers_deque = deque([source, ])
            elif isinstance(source, Iterable):
                self._numbers_deque = deque(source)

        self.to_number = to_number

    def __repr__(self):
        return '<Plivo api_url: %s, to_number: %s, source: %s>' % (
                self.api_url, self.to_number, self._numbers_deque)

    def get_numbers(self):
        pick_one = self._numbers_deque[0]
        self._numbers_deque.rotate(1)
        return pick_one

    @staticmethod
    def format_number(number):
        return number.strip().replace('+', '')

    def _requests(self, method, endpoint, data=None, json_format=True):
        ''' requests wraps '''
        auth = (self.auth_id, self.auth_token)
        headers = {'Connection': 'Keep-Alive'}

        if json_format:
            headers.update({'content-type': 'application/json'})
            data = json.dumps(data)

        if method == 'POST':
            result = requests.post(endpoint, data=data, auth=auth, headers=headers)
        elif method == 'GET':
            result = requests.get(endpoint, params=data, auth=auth, headers=headers)
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
        if 'src' not in data:
            data['src'] = self.get_numbers()

        endpoint = urljoin(self.api_url, 'Account/%s/Message/' % self.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def make_call(self, data):
        ''' Make a call
            Ref: http://plivo.com/docs/api/call/

            :rtype: dict
        '''
        if 'to' not in data:
            data['to'] = self.to_number
        if 'from' not in data:
            data['from'] = self.get_numbers()

        endpoint = urljoin(self.api_url, 'Account/%s/Call/' % self.auth_id)
        result = self._requests('POST', endpoint, data)
        return result

    def get_sms(self, message_uuid=None, params=None):
        ''' Get SMS info.
            Ref: http://plivo.com/docs/api/message/

            :rtype: dict
        '''
        endpoint = urljoin(self.api_url, 'Account/%s/Message/' % self.auth_id)

        if message_uuid:
            endpoint = urljoin(endpoint, message_uuid)

        result = self._requests('GET', endpoint, params, False)
        return result

    def get_all_sms(self, params=None):
        ''' Get all SMS log data '''
        log_data = self.get_sms(params=params)
        result = log_data['objects']

        while log_data['meta']['next']:
            log_data = self._requests('GET', urljoin(self.api_url,
                    log_data['meta']['next']))
            #result.extend(log_data['objects'])
            yield log_data['objects']

        #return result

    def get_account(self):
        ''' Get Account info
            Ref: http://plivo.com/docs/api/account/

            :rtype: dict
        '''
        endpoint = urljoin(self.api_url, 'Account/%s' % self.auth_id)
        result = self._requests('GET', endpoint)
        return result

if __name__ == '__main__':
    import setting
    #from datetime import datetime
    from pprint import pprint
    #text = u'這是一封測試簡訊 This a test SMS.'*2
    #data = {
    #        'src': setting.msg_from,
    #        'dst': setting.msg_to,
    #        'text': text + str(len(text)),
    #        'url': urljoin(setting.callback_url, 'message'),
    #       }
    PLIVO_TOOLS = Plivo(setting.auth_id, setting.auth_token,
            to_number=setting.msg_to, source=setting.msg_from)

    print PLIVO_TOOLS

    # ----- send sms ----- #
    #pprint(PLIVO_TOOLS.send_sms(data))

    # ----- Get Account info ----- #
    #t1 = datetime.now()
    #pprint(PLIVO_TOOLS.get_account())
    #print datetime.now() - t1
    #pprint(PLIVO_TOOLS.get_account())
    #print datetime.now() - t1

    # ----- get sms ----- #
    #pprint(PLIVO_TOOLS.get_sms(params={'limit': 5}))
    # /v1/Account/xxxxx/Message/?limit=20&%7B%22limit%22%3A5%7D=&offset=20
    #pprint(PLIVO_TOOLS.get_sms('f12115e4-891b-11e3-944e-1231400195a3'))

    # ----- get all sms ----- #
    all_sms = PLIVO_TOOLS.get_all_sms()
    print all_sms.next()

    # ----- make call ----- #
    #data = {
    #    'from': setting.msg_from,
    #    'to': setting.msg_to,
    #    'answer_url': setting.callback_url,
    #    'answer_method': 'GET',
    #    'hangup_method': 'GET',
    #    'fallback_method': 'GET',
    #    'caller_name': 'TESTHEROKU',
    #   }
    #make_call = PLIVO_TOOLS.make_call(data)
    #pprint(make_call) # request_uuid
