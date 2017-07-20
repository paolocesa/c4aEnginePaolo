import math
import random as rnd
from datetime import datetime, timedelta


def controlMsgsDay(messages, aged, max_msgs_day=5, max_same_resource=2):
    '''
    For every day schedules the messages to respect the following rules:
    less than max_msgs_day messages per day
    less than max_sam_resource messages per resource per day
    not after expiration date of the message
    :param messages: dict with all the messages of a user
    :return: dict with the messages scheduled
    '''
    timezero = datetime.strptime('00:00:00', '%H:%M:%S').time()

    '''
    for m in messages:
        print 'day ' + str(m)
        for mj in messages[m]:
            print str(mj.miniplan_id) + ' ' + str(mj.time.time())
            print 'Dates: ' + str(mj.date) + ' ' + str(mj.expiration_date)
            print
        print
    '''

    for day in sorted(messages.keys()):

        for m in messages[day]:
            c = 0
            to_del = []
            for mj in messages[day]:

                if m.miniplan_id == mj.miniplan_id:
                    c += 1

                if c > max_same_resource and m.miniplan_id == mj.miniplan_id and mj.final is False:
                    if day + timedelta(days=1) not in messages:
                        mj.date = datetime.combine(day + timedelta(days=1), timezero)
                        messages[day + timedelta(days=1)] = [mj]
                        to_del.append(mj)
                    else:
                        mj.date = datetime.combine(day + timedelta(days=1), timezero)
                        messages[day + timedelta(days=1)].append(mj)
                        to_del.append(mj)

            for d in to_del:
                messages[day].remove(d)

        if len(messages[day]) > max_msgs_day:

            for m in messages[day]:
                # move the messages that are scheduled al least 2 days before their expiration date
                if (m.expiration_date - day) > timedelta(days=2) and m.final is False:
                    if day + timedelta(days=1) not in messages:
                        messages[day].remove(m)
                        m.date = datetime.combine(day + timedelta(days=1), timezero)
                        messages[day + timedelta(days=1)]=[m]

                    else:
                        messages[day].remove(m)
                        m.date = datetime.combine(day + timedelta(days=1), timezero)
                        messages[day + timedelta(days=1)].append(m)

                if len(messages[day]) <= max_msgs_day:
                    break

            # if the previous condition is not enough move the messages with only one day of margin to the expiration date
            if len(messages[day]) > max_msgs_day:

                for m in messages[day]:

                    if (m.expiration_date - day) > timedelta(days=1) and m.final is False:
                        if day + timedelta(days=1) not in messages:
                            messages[day].remove(m)
                            m.date = datetime.combine(day + timedelta(days=1), timezero)
                            messages[day + timedelta(days=1)]=[m]

                        else:
                            messages[day].remove(m)
                            m.date = datetime.combine(day + timedelta(days=1), timezero)
                            messages[day + timedelta(days=1)].append(m)

                    if len(messages[day]) <= max_msgs_day:
                        break

        messages[day] = controlMsgsPerHour(messages[day],aged.hour_preference)

    '''
    for m in messages:
        print 'day after ' + str(m)
        for mj in messages[m]:
            print str(mj.miniplan_id) + ' ' + str(mj.time)
            print 'Dates: ' + str(mj.date) + ' ' + str(mj.expiration_date)
            print
        print
    '''


def controlMsgsPerHour(messages_same_day, pref=None):
    '''
    If two messages have less than one hour between them calls scheduleMessagesInDay that equally distributes all the 
    messages in the day, else let the times like they were
    :param messages_same_day: a list with the messages in the same day
    :return: the list with the updated times
    '''
    for i in range(1, len(messages_same_day)):
        if messages_same_day[i].time - messages_same_day[i - 1].time < timedelta(hours=1):
            messages_same_day = scheduleMessagesInDay(messages_same_day, pref)
            return messages_same_day

    return messages_same_day


def scheduleMessagesInDay(messages_same_day, pref=None):
    '''
    Evenly distributes the number of messages in the interval set by the pref param
    :param messages_same_day: the messages in a day
    :param pref: user preferences for the time to send the messages
    :return: the messages distributed
    '''

    begin = 8
    interval = 12 / float(len(messages_same_day))
    min_to_rand = 60

    if pref == '1':
        begin = 12
        interval = 8 / float(len(messages_same_day))
        min_to_rand = 40
    if pref == '0':
        interval = 4 / float(len(messages_same_day))
        min_to_rand = 20

    beginoftheworld = datetime.strptime('1900-01-01', '%Y-%m-%d')
    minutes = str(rnd.randrange(0, 59))
    messages_same_day[0].time = datetime.strptime(str(begin) + ':' + minutes, '%H:%M').time()
    messages_same_day[0].time = datetime.combine(beginoftheworld.date(), messages_same_day[0].time)

    for i in range(1, len(messages_same_day)):
        hours = math.modf(begin + i * interval)
        minutes = hours[0] * 60
        minutes = rnd.randrange(0, min_to_rand) + minutes
        h = hours[1]

        if minutes > 60:
            h += 1
            minutes -= 60
        messages_same_day[i].time = datetime.strptime(str(int(h)) + ':' + str(int(minutes)), '%H:%M').time()
        messages_same_day[i].time = datetime.combine(beginoftheworld.date(), messages_same_day[i].time)

    return messages_same_day
