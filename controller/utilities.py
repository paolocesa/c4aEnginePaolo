# !/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import pendulum
import json

from model.Aged import Aged
from model.Message import Message
from model.Resource import Resource
from model.Template import Template


def mapDay(on_day):
    day_of_event = None
    if on_day == 'Monday':
        day_of_event = 0
    elif on_day == 'Tuesday':
        day_of_event = 1
    elif on_day == 'Wednesday':
        day_of_event = 2
    elif on_day == 'Thursday':
        day_of_event = 3
    elif on_day == 'Friday':
        day_of_event = 4
    elif on_day == 'Saturday':
        day_of_event = 5
    elif on_day == 'Sunday':
        day_of_event = 6
    return day_of_event


def convertDatetime(request, template, resource):
    '''
    Converts request.from request.to and template.period in datetimes
    :param resource: a resource class
    :param request: a request class
    :param template: a template class
    :return: 3 datetimes from from_date,to_date and period
    '''
    expirationtime = None
    startime = datetime.strptime(request.from_date, '%d %b %Y')
    endtime = datetime.strptime(request.to_date, '%d %b %Y')
    if resource.to_date != None:
        expirationtime = datetime.strptime(resource.to_date, '%d %b %Y')
    period = timedelta(days=template.period * 7)

    return startime, endtime, period, expirationtime


def convertPendulum(request, template, resource):
    '''
    Converts request.from request.to and template.period in pendulum
    :param resource: a resource class
    :param request: a request class
    :param template: a template class
    :return: 3 pendulum from from_date,to_date and period
    '''
    expirationtime = None
    print type(request.from_date)
    startime = pendulum.parse(request.from_date)
    endtime = pendulum.parse(request.to_date)
    if resource.to_date != None:
        expirationtime = pendulum.parse(resource.to_date)
    period = pendulum.Period(startime, startime.add(weeks=template.period))

    return startime, endtime, period, expirationtime


def shiftMiniplan(miniplan, shift):
    shift = timedelta(days=shift)
    for i in range(0, len(miniplan)):
        miniplan[i].date = miniplan[i].date + shift
    return miniplan


def checkMsgsOneDay(miniplan, endtime):
    '''
    Pops the empty messages from the miniplan(if it has found <nmsg with getlistmessages)
    :param miniplan: a miniplan(list of messages)
    :param endtime: a datetime
    :return: a miniplan(list of messages)
    '''
    c = 0
    for i in range(0, len(miniplan)):
        if miniplan[i].date == None:
            c += 1

	'''
        elif miniplan[i].date == miniplan[i - 1].date:
            miniplan[i].date += timedelta(days=1)

            if miniplan[i].date > endtime.date():
                miniplan[i].date -= timedelta(days=1)
                miniplan[i - 1].date -= timedelta(days=1)
	'''

    while c > 0:
        miniplan.pop()
        c -= 1

    return miniplan


def checkMsgsOneDayPendulum(miniplan, endtime):
    '''
    Pops the empty messages from the miniplan(if it has found <nmsg with getlistmessages)
    :param miniplan: a miniplan(list of messages)
    :param endtime: a Pendulum
    :return: a miniplan(list of messages)
    '''
    c = 0
    for i in range(0, len(miniplan)):
        if miniplan[i].date == None:
            c += 1

        elif miniplan[i].date == miniplan[i - 1].date and miniplan[i].date == miniplan[i - 2].date:
            miniplan[i].date = miniplan[i].date.add(days=1)
            if miniplan[i].date > endtime.date():
                miniplan[i].date = miniplan[i].date.subtract(days=1)
                miniplan[i - 1].date = miniplan[i - 1].date.subtract(days=1)

    while c > 0:
        miniplan.pop()
        c -= 1

    return miniplan


def rebuildMiniplans(all_messages):
    '''
    This function builds a dictionary with key=miniplan_id given a dictionary that has messages with different miniplan_id
    :param all_messages: dict of messages
    :return: dict of messages with key=miniplan_id
    '''
    miniplans = {}
    for m in all_messages:
        m.date = m.date
        m.time = m.time
        if m.miniplan_id not in miniplans:
            miniplans[m.miniplan_id] = [m]
        else:
            miniplans[m.miniplan_id].append(m)
    return miniplans


def mapMessage(message_dict):
    message = Message(message_dict['message_id'], message_dict['user_id'], message_dict['intervention_session_id'])
    message.URL = message_dict['URL']
    message.attached_media = message_dict['attached_media']
    message.attached_audio = message_dict['attached_audio']
    message.channel = message_dict['channel']
    message.message_text = message_dict['message_text']
    message.miniplan_id = message_dict['miniplan_id']
    message.pilot_id = message_dict['pilot_id']
    if message_dict['date'] != '':
        message.date = datetime.strptime(message_dict['date'], '%Y-%m-%d')
    if message_dict['time'] != '':
        message.time = datetime.strptime(message_dict['time'], '%H:%M:%S')
    return message


def mapResource(res_dict):
    '''
    Maps a resource dictionary to a resource class
    :param res_dict: a resource dict
    :return: a resource class
    '''
    resource = Resource(res_dict['R_ID'])
    resource.url = res_dict['URL']
    resource.name = res_dict['Resource_Name']
    resource.media = res_dict['Media']
    resource.language = res_dict['Language']
    resource.category = res_dict['Category']
    resource.description = res_dict['Description']
    resource.subjects = res_dict['Subjects']
    resource.has_messages = res_dict['Has_messages']
    resource.partner = res_dict['Partner']
    resource.periodic = res_dict['Periodic']
    resource.translated = res_dict['Translated']
    resource.on_day = res_dict['On_day']
    resource.every = res_dict['Every']
    resource.repeating_time = res_dict['Repeating_time']
    if res_dict['From date'] != '':
        resource.from_date = datetime.strptime(res_dict['From date'], '%d/%m/%Y')
    if res_dict['To date'] != '':
        resource.to_date = datetime.strptime(res_dict['To date'], '%d/%m/%Y')
    return resource


def mapTemplate(temp_dict):
    '''
    Maps a template dictionary to a template class
    :param temp_dict: a template dict
    :return: a template class
    '''
    template = Template(temp_dict['ID'])
    template.category = temp_dict['Categoria']
    template.title = temp_dict['Titolo del template']
    template.description = temp_dict['Descrizione']
    template.nmsgmin = int(temp_dict['Numero di messaggi (min)'])
    template.nmsgmax = int(temp_dict['Numero di messaggi (max)'])
    template.period = float(temp_dict['Durata (settimane)'])
    template.channels = temp_dict['Canale'].split(', ')
    return template


def mapProfile(aged_dict):
    '''
    Maps a aged dictionary to a aged class
    :param aged_dict: a aged dict
    :return: a aged class
    '''
    aged = Aged(int(aged_dict['ID']))
    aged.name = aged_dict['name']
    aged.channels = aged_dict['channels'].split(', ')
    if aged_dict['hour_preference'] == 'None':
        aged.hour_preference = None
    else:
        aged.hour_preference = aged_dict['hour_preference']
    return aged


def getApipath():
    cfg = open('/home/hoclab/http/c4aengines/controller/config.cfg', 'r')
    for line in cfg:
        words = line.split(' ')
        if words[0] == 'ApiPath:':
            apipath = words[1].rstrip('\n')

    cfg.close()
    return apipath


def getDeliverypath():
    cfg = open('/home/hoclab/http/c4aengines/controller/config.cfg', 'r')
    for line in cfg:
        words = line.split(' ')
        if words[0] == 'DeliveryPath:':
            deliverypath = words[1].rstrip('\n')

    cfg.close()
    return deliverypath


def encodeMessage(message):
    dict = {}
    dict['miniplan_id'] = message.miniplan_id
    dict['intervention_session_id'] = message.intervention_session_id
    dict['pilot_id'] = message.pilot_id
    dict['time_2'] = message.time_2
    dict['time_1'] = message.time_1
    dict['time'] = message.time
    dict['message_id'] = message.message_id
    dict['channel'] = message.channel
    dict['user_id'] = message.user_id
    dict['date'] = message.date
    dict['expiration_date'] = message.expiration_date
    dict['attached_audio'] = message.attached_audio
    dict['attached_media'] = message.attached_media
    dict['message_text'] = message.message_text.replace("'", " ")
    dict['URL'] = message.URL
    return dict


def decodeMessage(dict):
    message = Message(dict['message_id'], dict['user_id'], dict['intervention_session_id'])
    message.miniplan_id = dict['miniplan_id']
    message.pilot_id = dict['pilot_id']
    message.time_2 = dict['time_2']
    message.time_1 = dict['time_1']
    message.time = dict['time']
    message.channel = dict['channel']
    message.date = dict['date']
    message.expiration_date = dict['expiration_date']
    message.attached_audio = dict['attached_audio']
    message.attached_media = dict['attached_media']
    message.message_text = dict['message_text']
    message.URL = dict['URL']
    return message

def decodeTemporaryMessage(dict):
    message = Message(dict['message_id'],1, dict['intervention_session_id'])
    message.miniplan_id = dict['miniplan_temporary_id']
    message.time = dict['range_hour_start']
    message.channel = dict['channel']
    message.date = dict['range_day_start']
    message.attached_audio = dict['audio']
    message.attached_media = dict['media']
    message.message_text = dict['text']
    message.URL = dict['url']
    return message

def dictToString(dict):
    return json.dumps(dict)
