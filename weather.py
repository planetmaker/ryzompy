#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:07:36 2020
Short python script to obtain weather prediction from ballistic mystics site
via its API

@author: planetmaker
"""

import requests
from argparse import ArgumentParser
import json
import pandas as pd

import matplotlib.pyplot as plt

import datetime

# # Prepare for website: https://towardsdatascience.com/how-to-easily-show-your-matplotlib-plots-and-pandas-dataframes-dynamically-on-your-website-a9613eff7ae3
# from flask import Flask, render_template, send_file, make_response, url_for, Response

# import io

# app = Flask(__name__)

apiurl = 'https://api.bmsite.net/atys/weather?cycles=39&offset=1'
show_duration_ingame = 36
update_frequency = 30  # Sekunden
api_frequency    = 60 # Sekunden
debug_level = 0

parser = ArgumentParser(description="Weather forecast for Ryzom")
parser.add_argument("-u", "--update", dest="update_frequency",
                    default=30, type=int,
                    help="update frequency for display")
parser.add_argument("-D", "--debug", dest="debug_level",
                    default=0, type=int,
                    help="debugging level (default = 0)")
args = parser.parse_args()

update_frequency = args.update_frequency

# print(args)
# print(args.debug_level)
# print(args.update_frequency)

translation_table = {
    'tryker':        {'name': 'Seenland', 'colour': 'blue'},
    'matis':         {'name': 'Wald',     'colour': 'green'},
    'fyros':         {'name': 'Wüste',    'colour': 'orange'},
    'zorai':         {'name': 'Dschungel','colour': 'fuchsia'},
#    'nexus':         'Nexus',
    'sources':       {'name':'Verbotene Quelle', 'colour': 'lightsteelblue'},
    'bagne':         {'name':'Abgrund von Ichor','colour': 'greenyellow'},
    'terre':         {'name':'Niemandsland',     'colour': 'sandybrown'},
    'route_gouffre': {'name':'Länder von Umbra', 'colour': 'lightpink'},
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

    global args
    def get_next_30(t):
        newt = t
        if t.minute < 30:
            newt = t.replace(minute = 30)
        else:
            # h = t.hour+1
            # d = t.day
            # if h >= 24:
            #     d = d + 1
            #     h = 0
            # newt = t.replace(minute = 0, hour=h, day=d)

            newt = t.replace(minute = 0, hour=t.hour, day=t.day)
            newt = newt + datetime.timedelta(hours=1)
        return newt

    t_ticks = trange
    dt =t_ticks[1] - t_ticks[0]
    if args.debug_level > 0:
        print(dt)
    rel_t_ticks = [0,1]

    newt = t_ticks[0]
    while get_next_30(newt) < trange[1]:
        newt = get_next_30(newt)
        # print(newt, trange[1])
        newdt = newt - t_ticks[0]
        reldt = newdt / dt
        trange.append(newt)
        rel_t_ticks.append(reldt)

    return trange, rel_t_ticks

def is_night(hour):
    h = hour % 24
    return h >= 22 or h <3

def is_dusk(hour):
    return (hour % 24) == 22

def get_nights(start_hour, duration):
    local_hour = time_of_day(start_hour)
    dusk = 22 - local_hour + start_hour
    if local_hour < 4:
        dusk -= 24
    nighttime = [(dusk, dusk + 5)]
    while dusk < start_hour + duration:
        dusk += 24
        nighttime.append((dusk, dusk+5))
    return nighttime

def on_close(event):
    print("Terminating Ryzom weather forecast")
    quit()

# #Pandas Page
# @app.route('/pandas', methods=("POST", "GET"))
# def GK():
#     return render_template('pandas.html',
#                            PageTitle = "Pandas",
#                            table=[GK_roi.to_html(classes='data', index = False)], titles= GK_roi.columns.values)


# #Matplotlib page
# @app.route('/matplot', methods=("POST", "GET"))
# def mpl():
#     return render_template('matplot.html',
#                            PageTitle = "Matplotlib")
# @app.route('/')
# @app.route('/weather.png')
# def plot_png():
#     fig=weather_plot()
#     output = io.BytesID()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

def weather_plot():
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
    nightdict = dict()
    first = True

    fig.canvas.mpl_connect('close_event', on_close)

    while True:
        rl_time = datetime.datetime.now()
        dt = (rl_time - old_rl_time).total_seconds()
        if args.debug_level > 0:
            print(rl_time, old_rl_time, dt)
        if dt > api_frequency or first:
            data = requests.get(apiurl)
            weather_json = json.loads(data.text)

            weather = dict()
            current_cycle = int(weather_json['cycle'])
            ingame_time  = float(weather_json['hour'])
            last_ingame_time = ingame_time
            old_rl_time = rl_time
        else:
            ingame_time = last_ingame_time + dt/180 #/3600 * 3600/180

        for item,value in translation_table.items():
            tmp = pd.DataFrame.from_records(weather_json['continents'][item]).T
            weather[item] = tmp.astype({'value': 'float64','cycle':'int64'})

        # Comparison to the ballistic mythics website:
        # There are added two flat hours, then an hour of change to the new value
        # The length of 8 weather cycles corresponds to the display on the website
        # 58400 weather cycles per year
        if (args.debug_level > 0):
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
            ax.plot(w2[item].index.values, w2[item]['value'], label=value['name'], color=value['colour'])
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

        nights = get_nights(ingame_time, show_duration_ingame)
        for night in nights:
            if night[0] not in nightdict:
                ax.axvspan(night[0],night[1], alpha=0.15, color='grey')
                nightdict[night[0]] = night

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

weather_plot()

# if __name__ == '__main__':
#     app.run(debug = True)