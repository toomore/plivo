# -*- coding: utf-8 -*-
import requests
import setting
from datetime import datetime
from plivo_api import Plivo
from pprint import pprint

def convertDate(datestr):
    return datetime.strptime(''.join(
            datestr.rsplit('+', 1)[:-1]), '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    PLIVO_TOOLS = Plivo(setting.auth_id, setting.auth_token)
    all_sms = PLIVO_TOOLS.get_all_sms()

    stop = False
    for sms_data in all_sms:
        pprint(sms_data)
        for i in sms_data:
            if convertDate(i['message_time']) <= datetime(2014, 3, 1):
                stop = True
                break

            print convertDate(i['message_time'])

        if stop:
            break
