#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:07:36 2020
Short python script to obtain weather prediction from ballistic mystics site
via its API

@author: planetmaker
"""

import requests
import json
import pandas as pd


apiurl = 'https://api.bmsite.net/atys/weather?cycles=8&offset=1'

translation_table = {
    'tryker':        'Seenland',
    'matis':         'Wald',
    'fyros':         'Wüste',
    'zorai':         'Dschungel',
    'nexus':         'Nexus',
    'sources':       'Urwurzeln',
    'bagne':         'Abgrund von Ichor',
    'terre':         'Niemandsland',
    'route_gouffre': 'Länder von Umbra',
    'newbieland':    'Silan',
    'kitiniere':     'Kitin-Nest'
    }

data = requests.get(apiurl)
weather_json = json.loads(data.text)

weather = dict()
for item,value in translation_table.items():
    tmp = pd.DataFrame.from_records(weather_json['continents'][item]).T
    weather[item] = tmp.astype({'value': 'float64','cycle':'int64'})

yticks = [0, 0.167, 0.334, 0.500, 0.666, 0.834]

# Comparison to the ballistic mythics website:
# There are added two flat hours, then an hour of change to the new value
# The length of 8 weather cycles corresponds to the display on the website
weather['zorai'].plot(x='cycle', y='value', grid='True', title='Wettervorhersage', yticks=yticks)

