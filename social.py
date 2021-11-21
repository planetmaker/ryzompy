#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 10:56:43 2021

@author: planetmaker
"""

import pandas as pd
import numpy as np
import scipy as sp

import math

import matplotlib.pyplot as plt


from datetime import datetime

global config
from social_config import config

"""
The logfile 'example.log' is expected to be a csv file in the following format:
"id","name","status","created_at"
"1","name1","offline","1632158674"
"2", "name2","online","1632158679"
...


The config itself specifies a few basic properties:

config =  = {
    "status_filename": 'example.log',
    "concurrency_jitter": 5,
    "status": {
        "offline": 0,
        "online": 1,
        },
    "timeframe": {
        "minimum": 0,            # 1.1.1970, 0:00h (unix time base)
        "maximum": 2637085847,   # far in the future
        },
    }


For fine-tuning parameters you can define a list of known sets of twinks,
thus each set contains character names played by the same player:
known_twinks = [("name_a1", "name_a2"), ("name_b1", "name_b2", "name_b3")]

Similarily you can define a list of names which you know are unique players:
known_distinct = ["name_a1", "name_c", "name_d"]
"""

seconds_per_day = 24 * 60 * 60
seconds_per_week = seconds_per_day * 7

class Character:
    """
    Contains the data about one character and low-level access
    """

    def __init__(self, name, time, status):
        self.name = name
        self.rawlog = dict()
        self.rawlog["status"] = [status]
        self.rawlog["time"] = [time]
        self.data = pd.DataFrame(data = None)
        self.data24h = pd.DataFrame(data = None)
        self.data7d = pd.DataFrame(data = None)

    def append_entry(self, time, status):
        self.rawlog["status"].append(status)
        self.rawlog["time"].append(time)

    def create_uniform_base(self, time_resolution = 1):
        n = len(self.rawlog["time"])

        time = list()
        status = list()
        for i in range(0, n-1):
            mint = self.rawlog["time"][i]
            maxt = self.rawlog["time"][i+1]
            value = self.rawlog["status"][i]
            dt = maxt - mint
            n_steps = math.floor(dt / time_resolution)
            time.extend([t + mint for t in range(0, n_steps, time_resolution)])
            status.extend([value] * n_steps)
        self.data["time"] = time
        self.data["status"] = status
        self.data["strg_date"]    = [datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S') for t in self.data["time"]]
        self.data["strg_weekday"] = [datetime.fromtimestamp(t).strftime('%a %H:%M:%S') for t in self.data["time"]]
        self.data["strg_time"]    = [datetime.fromtimestamp(t).strftime('%H:%M:%S') for t in self.data["time"]]

    def fold(self, timebase_name, duration, df):
        if "time" not in self.data:
            self.create_uniform_base()

        self.data[timebase_name] = self.data["time"] % duration
        df["time"] = [t for t in range(0, duration)]

    def fold_24hours(self):
        """
        Creates a 24-hour foleded status view for a person
        It requires the presence of a uniform (time) base which
        will be created, if not present. Default temporal spacing is 1s.

        Returns
        -------
        None.
        Creates:
            self.data24h["time"]          # array of time covering 24h
            self.data24h["status"]        # array of status covering 24h (cumulative)
            self.data24h["days"]          # array of number of days stacked for status
        """
        self.fold("time24h", seconds_per_day, self.data24h)
        self.data["strg_time"]    = [datetime.fromtimestamp(t).strftime('%H:%M:%S') for t in self.data["time"]]

    def fold_weekly(self):
        """
        Creates a weekly foleded status view for a person
        It requires the presence of a uniform (time) base which
        will be created, if not present. Default temporal spacing is 1s.

        Returns
        -------
        None.
        Creates:
            self.data7d["time"]          # array of time covering 24h
            self.data7d["status"]        # array of status covering 24h (cumulative)
            self.data7d["days"]          # array of number of days stacked for status
        """
        self.fold("time7d", seconds_per_week, self.data7d)
        self.data["strg_time"] = [datetime.fromtimestamp(t).strftime('%a %H:%M:%S') for t in self.data["time"]]


    def create_time_strings(self):
        """
        Creates human-readable timestamps from the unix timestamps (column 'time')

        Returns
        -------
        None.

        """
        self.data["timestrg"] = datetime.fromtimestamp(self.data["time"]).strftime('%Y-%m-%d %H:%M:%S')


    def plot_online(self, tmin=0, tmax=config["timeframe"]["maximum"]):
        fig, ax = plt.subplots()
        ax.step(self.rawlog["time"], self.rawlog["status"], linewidth=2.5)
        # ax.set(xlim=(config["timeframe"]["minimum"], config["timeframe"]["maximum"]))
        plt.show()



def read_status(filename):
    """
    Parameters
    ----------
    filename : string
        csv dump of the status data.

    Returns
    ----------
    content of the filename as pandas table

    """
    df = pd.read_csv(filename)
    return df

def status_to_numeric(str):
    """


    Parameters
    ----------
    str : string
        status as string from csv

    Returns
    -------
    status as numeric (see config)

    """
    num = np.NaN
    if str in config["status"]:
        num = config["status"][str]

    return num

def convert_raw(raw):
    """
    Parameters
    ----------
    raw : pandas data frame of the raw status data
        columns as indicated above for the logfile, but in proper format

    Returns
    ----------
    A dictionary of @Characters
    """
    characters = dict()
    for index in raw.index:
        name = raw["name"][index]
        status = status_to_numeric(raw["status"][index])
        time = raw["created_at"][index]

        if name in characters:
            characters[name].append_entry(time, status)
        else:
            characters[name] = Character(name, time, status)

    return characters


if __name__ == '__main__':
    global personal_log # make available to cmd for individual analysis
    raw_status = read_status(config["status_filename"])
    pl = convert_raw(raw_status)



