#!/usr/bin/python
# -*- coding: utf-8 -*-

class Template:
    def __init__(self, template_id, category="", title="", description="", addressed_to="", nmsgmin=0, nmsgmax=0,
                 period=0, channels=[],
                 compulsory="No", flowchart=None):
        self.template_id = template_id
        self.category = category
        self.title = title
        self.description = description
        self.nmsgmin = nmsgmin
        self.nmsgmax = nmsgmax
        self.period = period
        self.channels = channels
        self.compulsory = compulsory
        self.flowchart = flowchart
        self.addressed_to = addressed_to
