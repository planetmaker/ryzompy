#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 18:58:04 2021

@author: planetmaker
"""

__license__ = """
socialgraph is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

socialgraph is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with NML; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

import math
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

from social_globals import seconds_per_day, seconds_per_week
from social_config import config

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
        self.data["time24hf"] = self.data["time24h"] / 3600
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
        self.data["time7df"] = self.data["time7d"] / 3600 / 24
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

    def plot_folded(self, col_time_float, n_bins, col_data, **kwargs):
        """

        Parameters
        ----------
        col_time_float : str
            column name for the folded time (floating numbers).
        n_bins : int
            Number bins to use in the histogram
        col_data : TYPE
            Data columns to show foleded over the period.

        Returns
        -------
        None.

        """
        try:
            self.data.hist(col_time_float, bins=n_bins, weights=self.data[col_data])
        except KeyError as e:
            print("Columns not found: ")
            print(e)
            return

        try:
            if 'title' in kwargs:
                plt.title(kwargs['title'])
            if 'xtitle' in kwargs:
                plt.xtitle(kwargs['xtitle'])
            if 'ytitle' in kwargs:
                plt.ytitle(kwargs['ytitle'])
        except (KeyError, NameError):
            print("Invalid argument")
            return


    def plot_24h(self):
        """
        Plot the average online status over a 24h period

        Returns
        -------
        None.

        """
        if not "time24hf" in self.data:
            self.fold_24hours()

        self.plot_folded("time24hf", 24*60, "status") # 1-minute bins

    def plot_week(self):
        """
        Plot the average online status folder over weekly

        Returns
        -------
        None.

        """
        if not "time7df" in self.data:
            self.fold_weekly()

        self.plot_folded("time7df", 7*8, "status") # 3-hour bins
