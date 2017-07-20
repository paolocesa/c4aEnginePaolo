#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import dumps

import requests
import os
import re
from controller.utilities import getDeliverypath


def sendIntervention(message, aged):
    '''
    Send to the delivery system the information to send the messages to the aged, 
    this one respondes with sent or scheduled
    :param message: the message to send
    :param aged: the aged that receives the message
    :return: the response of the delivery system
    '''
    if message.channel == "SMS":
        params = {"user": "LCC", "pass": "274a54de7d27dbfb66780c8c4b4dd947bc9ed00106cd96863c8e38937c7a1eaf",
                  "channel": "sms",
                  "mode": "relay",
                  "to": aged.mobile_phone_number,
                  "msg": message.message_text.encode('utf8').replace("'"," "),
                  "sendTime": message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()
	print r

    elif message.channel == 'Email':

        params = {"user": "LCC", "pass": "274a54de7d27dbfb66780c8c4b4dd947bc9ed00106cd96863c8e38937c7a1eaf",
                  "channel": "email",
                  "mode": "relay",
                  "to": aged.email,
                  "msg": message.message_text,
                  "sendTime": message.date + " " + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Telegram':

        params = {'user': 'LCC', 'pass': '274a54de7d27dbfb66780c8c4b4dd947bc9ed00106cd96863c8e38937c7a1eaf',
                  'channel': 'telegram',
                  'mode': 'relay',
                  'to': aged.telegram,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Facebook':

        params = {'user': 'LCC', 'pass': '274a54de7d27dbfb66780c8c4b4dd947bc9ed00106cd96863c8e38937c7a1eaf',
                  'channel': 'fbm',
                  'mode': 'relay',
                  'to': aged.facebook,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Whatsapp':

        params = {'user': 'LCC', 'pass': '274a54de7d27dbfb66780c8c4b4dd947bc9ed00106cd96863c8e38937c7a1eaf',
                  'channel': 'whatsapp',
                  'mode': 'relay',
                  'to': aged.mobile_phone_number,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    return r
