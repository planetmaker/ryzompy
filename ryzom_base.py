#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:01:20 2020

@author: planetmaker
"""

from enum import Enum


ryzom_base_url      = "https://api.ryzom.com/"
ryzom_api_endpoints = {
    'character': {'url': "character.php", 'params': ['apikey']},
    'guild':     {'url': "guild.php", 'params': ['apikey']},
    }

def compose_ryzom_api_url(endpoint, params=[]):
    try:
        url = ryzom_api_endpoints[endpoint]['url']
    except:
        return None

    if params is list():
        return url

    for num,param in enumerate(params):
        c = '?' if num == 1 else '&'

        if param[0] in ryzom_api_endpoints[endpoint]['params']:
            try:
                url += c + param[0] + "=" + param[1]
            except:
                pass

    return url


class API_error(Enum):
    INVALID_API_KEY = 404
    KEY_EXPIRED     = 403
    NOT_INITIALIZED = 503 # for both character and guild

class Colour(Enum):
    undefined = -1
    red       = 0
    beige     = 1
    orange    = 2
    green     = 3
    turquoise = 4
    blue      = 5
    purple    = 6
    white     = 7
    black     = 8

class Ecosystem(Enum):
    undefined = 0
    desert    = 1
    wood      = 2
    lake      = 3
    jungle    = 4
    roots     = 6

class Race(Enum):
    Tryker    = 0
    Matis     = 1
    Fyros     = 2
    Zorai     = 3
