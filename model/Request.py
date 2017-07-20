#!/usr/bin/python
# -*- coding: utf-8 -*-

class Request:
    def __init__(self, request_id, pilot_id, intervention_session_id, resource_id, template_id, aged_id, miniplan, category="",
                 resource="", subjects="",
                 from_date=None, to_date=None):
        self.request_id = request_id
        self.resource_id = resource_id
        self.pilot_id = pilot_id
        self.intervention_session_id = intervention_session_id
        self.template_id = template_id
        self.aged_id = aged_id
        self.category = category
        self.resource = resource
        self.subjects = subjects
        self.from_date = from_date
        self.to_date = to_date
        self.miniplan = miniplan
