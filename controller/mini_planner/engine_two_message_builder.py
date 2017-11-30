#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from controller.mini_planner.Logica import readXML, evaluateRules
import json
import re

def generate_message_text(user, main_text, url):
    '''
    Returns the text of the message
    :param user: user class to use user hour preference to choose the greeting and to use the name to substitute the variables
    :param main_text: text of the message to modify
    :return: the text of the message with the greetings and the variables
    '''
    complete_text = ''

    greetings = {
        None: ['Ciao ' + user.name +'!',
               'Ben ritrovato ' + user.name + ':)',
               'Salve ' + user.name + '!',
               'Ciao ' + user.name + '! Che bella giornata, vero?',
               user.name + ', come stai?',
               user.name + ':) Oggi ho un\'interessante notizia da condividere con te!',
               'Ciao ' + user.name + ', cosa stai facendo?'],

        '1': ['Buonasera ' + user.name + '!',
              'Buon pomeriggio ' + user.name + '!'],

        '0': ['Buongiorno ' + user.name + '!',
              'Buon mattino ' + user.name + '!']}

    for greeting in greetings:
        if greeting == user.hour_preference:
            complete_text += (random.choice(greetings[greeting]))

    complete_text += ' ' + main_text
    complete_text += ' ' + url

    return complete_text


def buildMessage(aged, resourceMessage):
    '''
        Returns the text of the message
        :param aged: aged class to use user hour preference to choose the greeting and to use the name to substitute the variables
        :param resourceMessage: resourceMessage class
        :return: the text of the message with the greetings and the variables
        '''
    complete_text = ''

    greetings = {
        None: ['Ciao ' + aged.name + '!',
               'Ben ritrovato ' + aged.name + ':)',
               'Salve ' + aged.name + '!',
               'Ciao ' + aged.name + '! Che bella giornata, vero?',
               aged.name + ', come stai?',
               aged.name + ':) Oggi ho un\'interessante notizia da condividere con te!',
               'Ciao ' + aged.name + ', cosa stai facendo?'],

        '1': ['Buonasera ' + aged.name + '!',
              'Buon pomeriggio ' + aged.name + '!'],

        '0': ['Buongiorno ' + aged.name + '!',
              'Buon mattino ' + aged.name + '!']}

    for greeting in greetings:
        if greeting == aged.hour_preference:
            complete_text += (random.choice(greetings[greeting]))

    if resourceMessage.text is not None:
        complete_text += ' ' + resourceMessage.text
    
    if resourceMessage.url is not None:
        complete_text += ' ' + resourceMessage.url

    return complete_text


def composeFormulations(closes_results, formulations, open_text):
    word_pieces = {}
    for w in formulations:
        close = formulations[w]['precondition']
        splitted_close = close.split(",")
        numCloses = len(splitted_close)
        results_multiplePrec = {}
        if numCloses > 1:
            for i in range(0, numCloses):
                results_multiplePrec[splitted_close[i]] = closes_results[splitted_close[i]]
            flagBrokenLoop = False
            for e in results_multiplePrec:
                if results_multiplePrec[e]== False:
                    flagBrokenLoop = True
                    break
            if flagBrokenLoop:
                hypotesis = False
            else:
                hypotesis = True
        else:
            hypotesis = closes_results[close]

        if hypotesis:
            word_pieces[w] = formulations[w]['consequence']
        else:
            if 'alternative' in formulations[w]:
                word_pieces[w] = formulations[w]['alternative']
    for t in open_text:
        for piece in word_pieces:
            if t == word_pieces[piece]:
                word_pieces[piece] = open_text[t]
    return word_pieces
def orderMessage(sentences):
    order = sentences['order']
    max_index = len(order)
    start_index = 1
    message_ordered = ""
    while start_index <= max_index:
        str_index = str(start_index)
        message_ordered = message_ordered + "{*"+order[str_index].encode('ascii','ignore')+"*}"
        start_index = start_index + 1
    return message_ordered
def replacePlaceHolders(message_text,data,word_data, order):
    #replace the body_placeholder of the message with the actual body
    final_msg = order.replace("{*body*}", message_text['body'])
    for w_var in word_data:
        if w_var != 'order':
            final_msg = final_msg.replace("{*" + w_var + "*}", str(word_data[w_var]))
    # once the message is ready, all the msg variables have to be filled with the right value
    for var in data:
        final_msg = final_msg.replace("[*" + var + "*]", str(data[var]))
    #check if there is still some {*w*} in the text and, in case, remove them
    p = re.compile('{\*\w+\*}')
    final_mex = p.sub('', final_msg)
    return final_mex
def composeMessage(profileData, resourceData, contextData, messageData):
    RULES_DOCUMENT = "rules.json"
    #get the information from all the xml needed
    profile = readXML(profileData)
    resource = readXML(resourceData)
    context = readXML(contextData)
    #merge everything together as 'data'
    data = {}
    data.update(profile)
    data.update(resource)
    if context is not None:
        data.update(context)
    #analyze how the message has to be built
    with open(messageData) as json_mex:
        message = json.load(json_mex)
        json_mex.close()
    #take the closes to be used
    closes_used = message['closes']
    #the text to be composed togethere
    text = message['open_text']
    #the formulations that specify the structure of the message
    forms = message['verbal_formulations']
    #evaluate the rules
    closesResults = evaluateRules(RULES_DOCUMENT, data)
    #form all the results, take only the one needed for this message
    neededResults = {}
    for c in closesResults:
        if c in closes_used:
            neededResults[c] = closesResults[c]
    #analyze the formulations and compose the peices of message
    msg_pieces = composeFormulations(neededResults, forms, text)
    #compose the message following the order defined in json
    order = orderMessage(msg_pieces)
    #replace all the placeholders to make the message more personal
    personal_msg = replacePlaceHolders(text, data, msg_pieces, order)
    return personal_msg

