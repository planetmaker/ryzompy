#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:01:20 2020

@author: planetmaker
"""

import requests
ryzom_base_url      = "https://api.ryzom.com/"
ryzom_api_endpoints = {
    'character': {'url': "character.php", 'params': ['apikey']},
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

class ryzomstats:

    def __init__(self):
        pass

