#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 16:41:30 2020

@author: planetmaker
"""

from ryzomstats import compose_ryzom_api_url

class player_inventory:

    apikey  = ''
    content = list()
    name    = ''
    place   = ''

    def __init__(self, apikey=apikey, name=name, place=place):
        if apikey:
            self.content = readapi_content_to_dict(apikey)
            self.apikey  = apikey
        if name:
            self.name = name
        if place:
            self.place = place

    def get_content_by_id(self, id):
        pass

    def get_content_by_name(self, name):
        pass

    def get_content_by_type(self, mat_type):
        pass

