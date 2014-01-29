# -*- coding: utf-8 -*-
import pprint
import requests
import setting


def send_sms(data):
    endpoint = 'https://api.plivo.com/v1/Account/%s/Message/' % setting.auth_id
    result = requests.post(endpoint, data=data,
                           auth=(setting.auth_id, setting.auth_token))
    return result

if __name__ == '__main__':
    text = u'這是一封測試簡訊 This a test SMS.'
    data = {
            'src': '',
            'dst': '',
            'text': text*2 + str(len(text*2)),
           }
    pprint(send_sms(data))
