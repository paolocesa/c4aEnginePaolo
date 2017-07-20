#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


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
