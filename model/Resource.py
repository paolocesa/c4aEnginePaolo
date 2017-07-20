#!/usr/bin/python
# -*- coding: utf-8 -*-

class Resource:
    def __init__(self, resource_id, category="", name="", subjects="", has_messages="", url="", partner="",
                 translated="", periodic="", repeating_time="", media="", language="", description="", every="",
                 on_day="", from_date=None,
                 to_date=None):
        self.resource_id = resource_id
        self.category = category
        self.name = name
        self.description = description
        self.url = url
        self.language = language
        self.media = media
        self.from_date = from_date
        self.to_date = to_date
        self.subjects = subjects
        self.has_messages = has_messages
        self.partner = partner
        self.translated = translated
        self.periodic = periodic
        self.repeating_time = repeating_time
        self.on_day = on_day
        self.every = every
