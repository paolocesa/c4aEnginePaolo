#!/usr/bin/python
# -*- coding: utf-8 -*-
import random as rnd
from datetime import datetime, date, timedelta


def scheduleHour(user, time):
    '''
    Returns the time to send the message, if time is not None the time is only changed to be in the range 8-20 else it
    generate a random time
    :param user: a user class
    :param time: a time
    :return: the time to send the message
    '''
    day = range(8, 20)
    morning = range(8, 12)
    afternoon = range(12, 20)
    minutes = str(rnd.randrange(0, 59))

    if time is None:
        if user.hour_preference is None:
            return datetime.strptime(str(rnd.choice(day)) + ':' + minutes, '%H:%M').time()
        elif user.hour_preference == "0":
            return datetime.strptime(str(rnd.choice(morning)) + ':' + minutes, '%H:%M').time()
        elif user.hour_preference == "1":
            return datetime.strptime(str(rnd.choice(afternoon)) + ':' + minutes, '%H:%M').time()
        else:
            print "User hour preference error"
            return
    else:
        if user.hour_preference is None:
            temp = datetime.combine(date.today(), time) + timedelta(hours=2)
            return temp.time()

        elif user.hour_preference == "0":
            temp = datetime.combine(date.today(), time) + timedelta(hours=2)
            if temp.time() > datetime.strptime('12:00', '%H:%M').time():
                return datetime.strptime('12:00', '%H:%M').time()
            else:
                return temp.time()

        elif user.hour_preference == "1":
            temp = datetime.combine(date.today(), time) + timedelta(hours=2)
            if temp.time() > datetime.strptime('23:59', '%H:%M').time():
                return datetime.strptime('23:59', '%H:%M').time()
            else:
                return temp.time()

        else:
            print "User hour preference error"
            return


def scheduleHourFromDate(user, date):
    '''
    Returns a date that has times between 8 and 20, depending on user hour preference, using the hour of the date
    passed
    :param user: a user class
    :param date: a date
    :return: the date with the time in the constraint
    '''
    morning = range(8, 12)
    afternoon = range(12, 20)
    minutes = str(rnd.randrange(0, 59))

    if user.hour_preference is None:
        if date.time() > datetime.strptime('20:00', '%H:%M').time():
            return date - timedelta(hours=4)
        elif date.time() < datetime.strptime('8:00', '%H:%M').time():
            return date + timedelta(hours=8)
        else:
            return date

    elif user.hour_preference == "0":
        if date.time() >= datetime.strptime('12:00', '%H:%M').time() or date.time() <= datetime.strptime('8:00',
                                                                                                         '%H:%M').time():
            return datetime.strptime(str(rnd.choice(morning)) + ':' + minutes, '%H:%M')
        else:
            return date

    elif user.hour_preference == "1":
        if date.time() <= datetime.strptime('12:00', '%H:%M').time() or date.time() >= datetime.strptime('20:00',
                                                                                                         '%H:%M').time():
            return datetime.strptime(str(rnd.choice(afternoon)) + ':' + minutes, '%H:%M')
        else:
            return date
