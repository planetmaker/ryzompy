#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 09:56:59 2020

@author: planetmaker
"""

from ryzomstats import baseurl

class guild():
    apikey = ''
    name   = ''


    def __init__(self, apikey=None, name=''):
        if apikey is not None:
            self.apikey = apikey
        self.name = name

    def get_icon_url(self):
        api_endpoint = '/guild_icon.php?icon=:icon&size=:size'