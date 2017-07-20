#!/usr/bin/python
# -*- coding: utf-8 -*-

class Message:
    def __init__(self, message_id, user_id, intervention_session_id, message_text="error",
                 URL=["www.google.com", "www.polimi.it"], attached_media=['Media1', 'Media2'],
                 attached_audio=['Audio1', 'Audio2'],
                 channel=None, date=None, time=None, pilot_id=1, miniplan_id=6, expiration_date=None, time_1=None,
                 time_2=None, final=False, status=None, temporary_id=None, video=None):
        self.pilot_id = pilot_id
        self.message_id = message_id
        self.user_id = user_id
        self.intervention_session_id = intervention_session_id
        self.message_text = message_text
        self.URL = URL
        self.attached_media = attached_media
        self.attached_audio = attached_audio
        self.channel = channel
        self.date = date
        self.time = time
        self.miniplan_id = miniplan_id
        self.expiration_date = expiration_date
        self.time_1 = time_1
        self.time_2 = time_2
        self.final = final
        self.status = status
        self.temporary_id=temporary_id
        self.video= video

