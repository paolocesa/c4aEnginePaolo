#!/usr/bin/python
# -*- coding: utf-8 -*-

class Aged:
    def __init__(self, aged_id, name="", surname="", channels="SMS", hour_preference=None, message_frequency=None,
                 communication_style=None, topics=None, address=None, telephone_home_number=None,
                 mobile_phone_number=None, email=None, facebook_account=None, telegram_account=None):
        self.aged_id = aged_id
        self.name = name
        self.surname = surname
        self.channels = channels
        self.hour_preference = hour_preference
        self.message_frequency = message_frequency
        self.communication_style = communication_style
        self.topics = topics
        self.address = address
        self.telephone_home_number = telephone_home_number
        self.mobile_phone_number = mobile_phone_number
        self.email = email
        self.facebook = facebook_account
        self.telegram = telegram_account
