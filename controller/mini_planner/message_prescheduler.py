#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import random as rnd
import uuid
from datetime import datetime, timedelta

import pendulum
from pendulum import Pendulum

from controller.get_data import getResourceMessages
from controller.mini_planner.define_channels import getChannelsAvailable
from controller.mini_planner.engine_two_message_builder import generate_message_text, buildMessage
from controller.mini_planner.hour_manager import scheduleHour, scheduleHourFromDate
from controller.mini_planner.message_selector import getListMessages, selectMessages
from controller.utilities import mapDay, convertDatetime, checkMsgsOneDay, convertPendulum, checkMsgsOneDayPendulum
from model.Message import Message


def schedule(request, resource, template, aged):
    errors = {}

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    if template.nmsgmin != template.nmsgmax and template.nmsgmax > template.nmsgmin:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    # creates miniplan that is a list of messages
    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    '''
    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)
    '''

    messages = getResourceMessages(resource.resource_id)
    msgs_tosend = selectMessages(messages, nmsg, channels)

    er = checkForErrors(errors, endtime, None, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    for i in range(0, lenloop):
        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])
        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

    miniplan = ED(miniplan, lenloop, startime, endtime, period, aged)

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def ED(miniplan, lenloop, startime, endtime, period, aged):
    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    step_send_msg = valid_interval / lenloop

    date = startime + (step_send_msg / 2)
    for i in range(0, lenloop):
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHour(aged, None)
        date += step_send_msg
    return miniplan


def L(miniplan, lenloop, startime, endtime, period, aged):
    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    for i in range(0, lenloop):
        date = endtime - valid_interval
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHourFromDate(aged, date).time()
        valid_interval = valid_interval / (i + 2)

    return miniplan


# TODO think how to make this work
'''
def P(miniplan, lenloop, startime, endtime, period, aged):
    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    day_of_event = mapDay(resource.on_day)
    if day_of_event == None:
        errors['ErrorNoDay'] = 'Error no day specified for periodic messages'
        miniplan = []
        return errors, miniplan
    
    c = 0
    i = 0
    for dt in valid_interval.range("days"):
        if dt.day_of_week == day_of_event:
            if c % int(resource.every) == 0:
                if i > lenloop:
                    break
                miniplan[i].date = dt.date()
                miniplan[i].time = scheduleHour(aged, None)
                i += 1
            c += 1
    
    return miniplan
'''


def scheduleEDPPendulum(request, resource, template, aged):
    '''
        Returns the miniplan with the temporal interval between the msgs divided equally with Pendulum
        :param request: a request class
        :param template: a template class
        :param aged: a user class
        :return: a miniplan that is a list of messages class with all the fields completed
        '''
    errors = {}
    miniplanID = uuid.uuid4()

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))

    valid_interval = endtime - startime
    if valid_interval > period:
        errors['Interval changed'] = 'Duration of the template(' + str(
            period) + ') less than interval set by the care giver'
        valid_interval = period

    if template.nmsgmin != template.nmsgmax and template.nmsgmax > template.nmsgmin:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    # creates miniplan that is a list of messages
    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    '''
    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)
    '''

    messages = getResourceMessages(resource.resource_id)
    if messages is None:
        errors = {'Error': 'Messages not found'}
        miniplan = {}
        return errors, miniplan

    msgs_tosend = selectMessages(messages, nmsg, channels)

    er = checkForErrors(errors, endtime, None, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    step_send_msg = valid_interval / lenloop

    date = startime + (step_send_msg / 2)
    for i in range(0, lenloop):
        miniplan[i].miniplan_id = miniplanID
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHour(aged, None)
        miniplan[i].message_text = buildMessage(aged, msgs_tosend[i])
        miniplan[i].attached_audio = msgs_tosend[i].audio
        miniplan[i].attached_media = msgs_tosend[i].media
        miniplan[i].URL = msgs_tosend[i].url
        miniplan[i].channel = msgs_tosend[i].channels[0]['channel_name']
        miniplan[i].time_1 = date.date()
        miniplan[i].time_2 = date.add(days=1).date()
        miniplan[i].intervention_session_id = request.intervention_session_id
        miniplan[i].pilot_id = request.pilot_id

        date += step_send_msg

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleLPendulum(request, resource, template, aged):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg with logaritmic growth:1 1/2 1/3 1/4
    Check on period(valid weeks): if request interval is larger that period then user period as interval
    Last message always sent the day before the event
    With Pendulum
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    errors = {}
    miniplanID = uuid.uuid4()

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    valid_interval = endtime - startime
    if valid_interval > period:
        errors['Interval changed'] = 'Duration of the template(' + str(
            period) + ') less than interval set by the care giver'
        valid_interval = period

    channels = getChannelsAvailable(template, aged)

    messages = getResourceMessages(resource.resource_id)
    if messages is None:
        errors = {'Error': 'Messages not found'}
        miniplan = {}
        return errors, miniplan

    msgs_tosend = selectMessages(messages, nmsg, channels)

    '''
    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)
    '''

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    for i in range(0, lenloop):
        date = endtime - valid_interval

        miniplan[i].miniplan_id = miniplanID

        miniplan[i].date = date.date()
        miniplan[i].time_1 = date.date()
        miniplan[i].time_2 = date.add(days=1).date()

        miniplan[i].time = scheduleHourFromDate(aged, date).time()

        miniplan[i].message_text = buildMessage(aged, msgs_tosend[i])

        miniplan[i].attached_audio = msgs_tosend[i].audio
        miniplan[i].attached_media = msgs_tosend[i].media
        miniplan[i].URL = msgs_tosend[i].url
        miniplan[i].message_id= msgs_tosend[i].message_id

        miniplan[i].channel = msgs_tosend[i].channels[0]['channel_name']

        miniplan[i].intervention_session_id = request.intervention_session_id
        miniplan[i].pilot_id = request.pilot_id

        valid_interval = valid_interval / (i + 2)

    miniplan = checkMsgsOneDayPendulum(miniplan, endtime)

    return errors, miniplan


def schedulePPendulum(request, resource, template, aged):
    errors = {}

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    miniplanID = uuid.uuid4()

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    day_of_event = mapDay(resource.on_day)
    if day_of_event == None:
        errors['ErrorNoDay'] = 'Error no day specified for periodic messages'
        miniplan = []
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    c = 0
    i = 0
    for dt in valid_interval.range("days"):
        if dt.day_of_week == day_of_event:
            if c % int(resource.every) == 0:
                if i > lenloop:
                    break
                miniplan[i].miniplan_id = miniplanID
                miniplan[i].date = dt.date()
                miniplan[i].time_1 = dt.date()
                miniplan[i].time_2 = dt.subtract(days=1).date()
                miniplan[i].time = scheduleHour(aged, None)
                miniplan[i].attached_audio = msgs_tosend[i]['Audio']
                miniplan[i].attached_media = msgs_tosend[i]['Media']
                miniplan[i].URL = msgs_tosend[i]['URL']

                miniplan[i].channel = msgs_tosend[i]['Channel']
                miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'],
                                                                 msgs_tosend[i]['URL'])

                miniplan[i].intervention_session_id = request.intervention_session_id
                miniplan[i].pilot_id = request.pilot_id

                i += 1
            c += 1

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleEquallyDividedPeriod(request, resource, template, aged):
    '''
    Returns the miniplan with the temporal interval between the msgs divided equally
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax
    step_send_msg = valid_interval / nmsg

    # creates miniplan that is a list of messages
    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, None, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    # for nmsg fill the miniplan msgs
    date = startime
    for i in range(0, lenloop):
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHour(aged, None)
        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])
        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        date += step_send_msg

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleLogarithmic(request, resource, template, aged):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg with logaritmic growth:1 1/2 1/3 1/4
    Check on period(valid weeks): if request interval is larger that period then user period as interval
    Last message always sent the day before the event
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    valid_interval = timedelta(seconds=valid_interval.total_seconds())
    for i in range(0, lenloop):
        date = endtime - valid_interval

        miniplan[i].date = date.date()

        miniplan[i].time = scheduleHourFromDate(aged, date).time()

        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])

        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        valid_interval = timedelta(seconds=valid_interval.total_seconds() / (i + 2))

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def schedulePeriodic(request, resource, template, aged):
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    valid_interval = endtime - startime
    if valid_interval > period:
        endtime = startime + period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    day_of_event = mapDay(resource.on_day)
    if day_of_event == None:
        errors['ErrorNoDay'] = 'Error no day specified for periodic messages'
        miniplan = []
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    c = 0
    i = 0
    current_date = startime.date()
    while current_date < endtime.date():
        if current_date.weekday() == day_of_event - 1:
            if c % int(resource.every) == 0:
                if i > lenloop:
                    break
                miniplan[i].date = current_date
                miniplan[i].time = scheduleHour(aged, None)
                miniplan[i].attached_audio = msgs_tosend[i]['Audio']
                miniplan[i].attached_media = msgs_tosend[i]['Media']
                miniplan[i].URL = msgs_tosend[i]['URL']
                miniplan[i].channel = msgs_tosend[i]['Channel']
                miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'],
                                                                 msgs_tosend[i]['URL'])
                i += 1
            c += 1

        current_date += timedelta(days=1)

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, msgs_tosend_len):
    if expirationtime != None:
        if endtime > expirationtime:
            endtime = expirationtime
            errors['ErrorEndtime'] = 'Endtime: spostato perchè resource finisce prima della data settata come endtime'
            return errors, miniplan, True, endtime
        elif startime > expirationtime:
            errors['ErrorExpiration'] = 'ERROR: start date dopo expiration date resource'
            return errors, miniplan, False

    if msgs_tosend_len == 0:
        errors['ErrorZeroMsg'] = 'Error: zero messaggi compatibili'
        miniplan = []
        return errors, miniplan, False

    if msgs_tosend_len < nmsg:
        errors['ErrorLessMsg'] = 'Numero di messaggi compatibili trovati minore del numero di messaggi da mandare'

    return errors, miniplan, True, endtime
