#!/usr/bin/python
# -*- coding: utf-8 -*-

class FlowchartMessage:
    def __init__(self, message_id, tag=None, time_1=None, time_2=None, conditions=None):
        self.message_id = message_id
        self.tag = tag
        self.time_1 = time_1
        self.time_2 = time_2
        self.conditions = conditions
