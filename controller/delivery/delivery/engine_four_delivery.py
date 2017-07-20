#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import dumps

import requests

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
        params = {"user": "C4A", "pass": "cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3",
                  "channel": "sms",
                  "mode": "relay",
                  "to": aged.mobile_phone_number,
                  "msg": message.message_text.encode('utf8').replace("'"," "),
                  "sendTime": message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()
        print r


    elif message.channel == 'Email':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'email',
                  'mode': 'relay',
                  'to': aged.email,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Telegram':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'telegram',
                  'mode': 'relay',
                  'to': aged.telegram,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Facebook':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'fbm',
                  'mode': 'relay',
                  'to': aged.facebook,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Whatsapp':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'whatsapp',
                  'mode': 'relay',
                  'to': aged.mobile_phone_number,
                  'msg': message.message_text,
                  'sendTime': message.date + ' ' + message.time}  # DD/MM/YYYY HH:mm

        print params
        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    return r
