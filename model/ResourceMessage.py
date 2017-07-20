#!/usr/bin/python
# -*- coding: utf-8 -*-

class ResourceMessage:
    def __init__(self, message_id, text=None, media=None, url=None, video=None, audio=None, semantic_type=None,
                 communication_style=None, is_compulsory=None, channels=None):
        self.message_id = message_id
        self.text = text
        self.media = media
        self.url = url
        self.video = video
        self.audio = audio
        self.semantic_type = semantic_type
        self.communication_style = communication_style
        self.is_compulsory = is_compulsory
        self.channels = channels
