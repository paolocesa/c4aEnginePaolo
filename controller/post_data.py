#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from pendulum import Date

from utilities import getApipath, encodeMessage, dictToString


def postMiniplanGenerated(miniplan_messages, req):
    '''
    Post miniplan just generated in the DB
    :param miniplan_messages: the miniplan
    :param req: the json request arrived
    :return: id of miniplan given by the DB
    '''

    params = {'generation_date': Date.today().to_date_string(), 'from_date': req.from_date.to_date_string(),
              'to_date': req.to_date.to_date_string(),
              'resource_id': req.resource_id, 'template_id': req.template_id,
              'intervention_id': req.intervention_session_id, 'is_committed': 'True','aged_id':req.aged_id,
              'miniplan_body': miniplan_messages, 'miniplan_id': req.miniplan}

    print params

    r = requests.post(getApipath() + "setNewMiniplanGenerated/", data=params).json()

    print r

    if 'new_id' in r[0]:
        return r[0]['new_id'], r[0]['temporary_id']


def postGeneratedMessage(message, jsonMessage):
    '''
    Post every message of the miniplan just generated in the DB
    :param message: the miniplan message
    :param jsonMessage: the message in json format
    :return: nothing
    '''
    paramsMessage = {'time_prescription': message.date, 'channel': message.channel,'media':message.attached_media,
                     'text': message.message_text,'url':message.URL,'video':message.video,
                     'audio': message.attached_audio,'status':'to send','message_id': message.message_id,
                     'range_day_start':message.date, 'range_day_end':message.date,
                     'range_hour_start': message.time.strftime("%H:%M"), 'range_hour_end':message.time.strftime("%H:%M"),
                     'generation_date': Date.today().to_date_string(),
                     'miniplan_generated_id': message.miniplan_id,
                     'intervention_session_id': message.intervention_session_id}

    print paramsMessage

    r = requests.post(getApipath() + "setNewMiniplanGeneratedMessage/", data=paramsMessage).json()

    print r


def postMiniplanFinal(temporaryMiniplan):
    '''
    Post miniplan just schedulued in the DB 
    :param miniplan_messages: the miniplan
    :param req: the json request arrived
    :return: id of miniplan given by the DB
    '''

    params = {'commit_date': Date.today().to_date_string(),
              'from_date': temporaryMiniplan['from_date'],
              'to_date': temporaryMiniplan['to_date'],
              'resource_id': temporaryMiniplan['temporary_resource_id'],
              'template_id': temporaryMiniplan['temporary_template_id'],
              'caregiver_id': '2',
              'intervention_id': temporaryMiniplan['intervention_session_id'],
              'generated_miniplan_id': temporaryMiniplan['miniplan_generated_id'],
              'miniplan_body': temporaryMiniplan['miniplan_body']}

    r = requests.post(getApipath() + "setNewMiniplanFinal/", data=params).json()

    if 'new_id' in r[0]:
        return r[0]['new_id']


def postFinalMessage(message):
    '''
    Post every message of the miniplan final in the DB
    :param message: the miniplan message
    :param jsonMessage: the message in json format
    :return: nothing
    '''

    paramsMessage = {'time_prescription': message.date, 'channel': message.channel, 'is_modified': 'False',
                     'message_body': dictToString(encodeMessage(message)), 'miniplan_id': message.miniplan_id, 'status': message.status,
                     'intervention_session_id': message.intervention_session_id}

    r = requests.post(getApipath() + "setNewMiniplanFinalMessage/", data=paramsMessage).json()

    print r
