#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import attrgetter

from pendulum import parse

from controller.delivery.engine_four_delivery import sendIntervention
from controller.get_data import getMessages, getAged
from controller.json_manager import encodePlan, encodeResponse
from controller.planner.controlConstraints import controlMsgsDay
from controller.post_data import postMiniplanFinal, postFinalMessage
from controller.utilities import rebuildMiniplans
from model.Aged import Aged


# TODO probably the messages are not scheduled correctly in the same day
def launch_engine_three(post_req):
    '''
    Launch the engine_three: the planner. schedules the messages of one user, it gets the messages 
    committed and puts it in the final messages scheduling in a smart way
    :param post_req: the post request
    :return: the plan of the user
    '''

    aged_id = post_req.form["aged_id"]
    errors = {}
    all_messages = []
    response = [{}, {}]
    dict_m = {}

    aged = getAged(aged_id)
    if aged is None:
        response[0] = {'Error': 'Aged not found'}
        response[1] = {}
        return encodeResponse(response[0], response[1])

    '''
    # substitute with getAged
    aged = Aged('1')
    aged.mobile_phone_number = '393297634573'
    aged.email = 'matteopasina@gmail.com'
    aged.facebook = 'https://www.messenger.com/t/1532723125/'
    '''

    # gets all the messages committed and final of a user
    (all_messages, temporaryMiniplans) = getMessages(aged_id)

    sorted_messages = sorted(all_messages, key=attrgetter('date', 'time'))

    for m in sorted_messages:
        if m.date not in dict_m:
            dict_m[parse(m.date)] = [m]
        else:
            dict_m[parse(m.date)].append(m)

    controlMsgsDay(dict_m, aged)

    miniplans = rebuildMiniplans(sorted_messages)

    # delivery
    for mini in miniplans:
        for m in miniplans[mini]:
            if m.final is False:
                #c+=1
                tempDate = parse(m.date)
                tempTime = parse(m.time)
                m.date = tempDate.format('DD/MM/YYYY', formatter='alternative')
                m.time = tempTime.format('HH:mm', formatter='alternative')
                interventionResponse = sendIntervention(m, aged)

    # post in DB
    for t in temporaryMiniplans:
        id_final = postMiniplanFinal(t)
        for mini in miniplans:
            for m in miniplans[mini]:
                if m.final is False and m.miniplan_id == str(t['miniplan_generated_id']):
                    m.miniplan_id = id_final
                    m.final = True
                    postFinalMessage(m)

    # writecsv(sorted_messages)

    return encodePlan(errors, sorted_messages)
