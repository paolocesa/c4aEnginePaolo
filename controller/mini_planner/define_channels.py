#!/usr/bin/python
# -*- coding: utf-8 -*-
import random as rnd

from numpy.random.mtrand import choice


def getChannelsAvailable(template, user):
    '''
    Intersects the lists of channels available for passed user and template
    :param template: template class
    :param user: user class
    :return: list of valid channels
    '''
    # channels = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getUser_Channel/id_user=' + user.user_id))
    # return [validChannel for validChannel in channels if validChannel in template.channels]
    if user.channels is None or template.channels is None:
        return []
    return [validChannel for validChannel in user.channels if validChannel in template.channels]


def channelWithProbability(channels):
    '''
    Returns a channel giving more weight based on the order of the list passed
    :param channels: list of channels available
    :return: the choosen channel
    '''
    channel_prob = []
    for j in range(0, len(channels)):
        l = len(channels) - j
        l *= l
        while l != 0:
            channel_prob.append(channels[j])
            l -= 1
    return rnd.choice(channel_prob)


# TODO fix, format?
def channelWithProbabilityNumpy(channels):
    '''
    Returns a channel giving more weight based on the order of the list passed using hard coded probability distribution
    :param channels: list of channels available
    :return: the choosen channel
    '''
    if len(channels) == 1:
        channel_prob = [1]
    elif len(channels) == 2:
        channel_prob = [0.7, 0.3]
    elif len(channels) == 3:
        channel_prob = [0.6, 0.3, 0.1]
    elif len(channels) == 4:
        channel_prob = [0.5, 0.25, 0.15, 0.1]
    elif len(channels) == 5:
        channel_prob = [0.45, 0.27, 0.13, 0.09, 0.04]
    print choice(channels, 1, p=channel_prob)
    return choice(channels, 1, p=channel_prob)
