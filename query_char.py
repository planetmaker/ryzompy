#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:15:36 2020

@author: planetmaker
"""

import requests

base_url = "https://api.ryzom.com/"

def queryCharacter(apikey):
    global base_url
    req = requests.post(base_url +  "character.php?apikey=" + apikey)
    # Response
    print(req)
    # Actual text as XML
    print(req.text)
    return req.text