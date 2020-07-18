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

import matplotlib.pyplot as plt
plt.close('all')


apiurl = 'https://api.bmsite.net/atys/weather?cycles=8&offset=1'

translation_table = {
    'tryker':        'Seenland',
    'matis':         'Wald',
    'fyros':         'Wüste',
    'zorai':         'Dschungel',
    'nexus':         'Nexus',
    'sources':       'Verbotene Quelle',
    'bagne':         'Abgrund von Ichor',
    'terre':         'Niemandsland',
    'route_gouffre': 'Länder von Umbra',
    'newbieland':    'Silan',
    'kitiniere':     'Kitin-Nest'
    }

data = requests.get(apiurl)
weather_json = json.loads(data.text)

def cycle_to_hour(c):
    """

    Parameters
    ----------
    c : int
        cycles number

    Returns
    -------
    int
        hour of day of the current cycle

    """
    return c * 3

def cycle_to_local_hour(c):
    return (c - c // 8 * 8) * 3

def time_of_day(current_hour):
    """
    Parameters
    ----------
    current_hour : float
        current hour as returned by ballistic mystics.

    Returns
    -------
    float
        time of day as floating point value of the hour

    """
    return current_hour - (current_hour // 24) * 24

weather = dict()
current_cycle = int(weather_json['cycle'])
ingame_time  = float(weather_json['hour'])

for item,value in translation_table.items():
    tmp = pd.DataFrame.from_records(weather_json['continents'][item]).T
    weather[item] = tmp.astype({'value': 'float64','cycle':'int64'})

yticks = [0, 0.167, 0.334, 0.500, 0.666, 0.834]
weather['zorai']['hour'] = cycle_to_hour(weather['zorai']['cycle'])

# ax = weather['zorai'].plot(x='hour', y='value', grid='True', title='Wettervorhersage', yticks=yticks)
# ax.axvline(x=ingame_time/3,ymin=0,ymax=1)

# Comparison to the ballistic mythics website:
# There are added two flat hours, then an hour of change to the new value
# The length of 8 weather cycles corresponds to the display on the website
# 58400 weather cycles per year
print("Cycle, hour, local hour: ",current_cycle, ingame_time, time_of_day(ingame_time))


iw = weather['zorai']
iw.set_index('hour', inplace=True)
iw2 = iw
for index, row in iw.iterrows():
    iw2.loc[index+1] = row
    iw2.loc[index+2] = row
iw2.sort_index(inplace=True)

w2 = dict()
w2['zorai'] = iw2
w2['zorai']['value'] = 100 * w2['zorai']['value']

yticks = [0, 16.7, 33.4, 50.0, 66.6, 83.4, 100]
xticks = w2['zorai'].index.values

ax = w2['zorai'].plot(y='value', grid='True', title='Wettervorhersage', yticks=yticks, xticks=xticks, label='Zorai', figsize=(12,5))
ax.axvline(x=ingame_time,ymin=0,ymax=1,color='red')

