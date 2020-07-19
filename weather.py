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

import datetime



apiurl = 'https://api.bmsite.net/atys/weather?cycles=39&offset=1'
show_duration_ingame = 36
update_frequency = 1  # Sekunden
api_frequency    = 60 # Sekunden



translation_table = {
    'tryker':        'Seenland',
    'matis':         'Wald',
    'fyros':         'Wüste',
    'zorai':         'Dschungel',
#    'nexus':         'Nexus',
    'sources':       'Verbotene Quelle',
    'bagne':         'Abgrund von Ichor',
    'terre':         'Niemandsland',
    'route_gouffre': 'Länder von Umbra',
#    'newbieland':    'Silan',
#    'kitiniere':     'Kitin-Nest'
    }

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
    return current_hour % 24

def time_to_tick_str(t):
    s = ""
    # s = str(t.hour) + ':' + str(t.minute) + 'h'
    s = "{0}:{1:02}h".format(t.hour, t.minute)
    return s

def get_rl_tick_times(trange):

    def get_next_30(t):
        newt = t
        if t.minute < 30:
            newt = t.replace(minute = 30)
        else:
            h = t.hour+1
            d = t.day
            if h >= 24:
                d = d + 1
                h = 0
            newt = t.replace(minute = 0, hour=h, day=d)
        return newt

    t_ticks = trange
    dt =t_ticks[1] - t_ticks[0]
    print(dt)
    rel_t_ticks = [0,1]

    newt = t_ticks[0]
    while get_next_30(newt) < trange[1]:
        newt = get_next_30(newt)
        print(newt, trange[1])
        newdt = newt - t_ticks[0]
        reldt = newdt / dt
        trange.append(newt)
        rel_t_ticks.append(reldt)

    return trange, rel_t_ticks







plt.close('all')
fig, ax = plt.subplots()
plt.grid(True)
plt.legend(loc='upper right')
fig.set_size_inches(12,5)
fig.subplots_adjust(bottom=0.25)

vertical_line_now = ax.axvline(x=0, color='red')

ax2 = ax.twiny()
ax2.xaxis.set_ticks_position("bottom")
ax2.xaxis.set_label_position("bottom")

ax2.spines["bottom"].set_position(("axes", -0.15))
ax2.set_frame_on(True)
ax2.patch.set_visible(False)
for sp in ax2.spines.values():
    sp.set_visible(False)
ax2.spines["bottom"].set_visible(True)

old_rl_time=datetime.datetime.now()
first = True
while True:
    rl_time = datetime.datetime.now()
    dt = (rl_time - old_rl_time).total_seconds()
    if dt > api_frequency or first:
        data = requests.get(apiurl)
        weather_json = json.loads(data.text)

        weather = dict()
        current_cycle = int(weather_json['cycle'])
        ingame_time  = float(weather_json['hour'])
    else:
        ingame_time = ingame_time + dt/180 #/3600 * 3600/180

    for item,value in translation_table.items():
        tmp = pd.DataFrame.from_records(weather_json['continents'][item]).T
        weather[item] = tmp.astype({'value': 'float64','cycle':'int64'})

    # Comparison to the ballistic mythics website:
    # There are added two flat hours, then an hour of change to the new value
    # The length of 8 weather cycles corresponds to the display on the website
    # 58400 weather cycles per year
    print("Cycle, hour, local hour: ",current_cycle, ingame_time, time_of_day(ingame_time))


    w2 = dict()
    for location in translation_table:
        weather[location]['hour'] = cycle_to_hour(weather[location]['cycle'])
        iw = weather[location]
        iw.set_index('hour', inplace=True)
        iw2 = iw
        for index, row in iw.iterrows():
            iw2.loc[index+1] = row
            iw2.loc[index+2] = row
        iw2.sort_index(inplace=True)

        w2[location] = iw2
        w2[location]['value'] = 100 * w2[location]['value']

    yticks = [0, 16.7, 33.4, 50.0, 66.6, 83.4, 100]
    xticks = w2['zorai'].index.values
    xticklabels = [time_of_day(x) for x in xticks]




    for item,value in translation_table.items():
        ax.plot(w2[item].index.values, w2[item]['value'], label=value)
    ax.set_xlabel('Ingame-Zeit')
    ax.set_ylabel('weather %')
    ax.set_title('Wettervorhersage')
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    # hack in order to not amend the legend anew each time
    if first:
        ax.legend(loc='upper right')

    ax.set_xticklabels(xticklabels)
    ax.set_xlim([ingame_time-1, ingame_time+show_duration_ingame])


    vertical_line_now.set_data([ingame_time, ingame_time], [0,1])


    ax2.set_xlim(0,1)
    t_min = rl_time - datetime.timedelta(minutes=3)
    t_max = rl_time + datetime.timedelta(minutes=3*show_duration_ingame)
    rl_times = [t_min, t_max]
    # print("time ranges: ",rl_times)
    t_tick_times, rel_tick_times = get_rl_tick_times(rl_times)
    # print(t_tick_times, rel_tick_times)
    ax2.set_xticks(rel_tick_times)
    t_tick_strs = [time_to_tick_str(t) for t in rl_times]
    ax2.set_xticklabels(t_tick_strs)
    ax2.set_xlabel("Real time")

    first = False
    plt.pause(update_frequency)

