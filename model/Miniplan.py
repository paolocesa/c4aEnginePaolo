#!/usr/bin/python
# -*- coding: utf-8 -*-

class Miniplan:
    def __init__(self, miniplan_id, to_date, message, intervention_session_id=1, resource_id=1,
                 template_id=1, generation_date=None, from_date=None):
        self.miniplan_id = miniplan_id
        self.generation_date = generation_date
        self.from_date = from_date
        self.to_date = to_date
        self.message = message
        self.intervention_session_id = intervention_session_id
        self.resource_id = resource_id
        self.template_id = template_id
