#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 10:56:43 2021

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
with socialgraph; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

import pandas as pd
import numpy as np

global config
from social_config import config
from character import Character

"""
The logfile 'example.log' is expected to be a csv file in the following format:
"id","name","status","created_at"
"1","name1","offline","1632158674"
"2", "name2","online","1632158679"
...

The logfile 'fight.log' is expected to be a csv file in the following format:
id,op,op_owner,op_owner_id,date,customer,customer_guild,attacking_guild,war_type,phase,created_at,created_by,modified_at,objective,comment


The config itself specifies a few basic properties:

config =  = {
    "status_filename": 'example.log',
    "fightlog_filename": 'fight.log',
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
        time = raw["created_at"][index]
        # skip processing, if the time is out of bounds
        if time < config["timeframe"]["minimum"] or time > config["timeframe"]["maximum"]:
            continue

        name = raw["name"][index]
        status = status_to_numeric(raw["status"][index])

        if name in characters:
            characters[name].append_entry(time, status)
        else:
            characters[name] = Character(name, time, status)

    return characters


if __name__ == '__main__':
    global personal_log # make available to cmd for individual analysis
    print("Using config:")
    print(config)

    raw_status = read_status(config["status_filename"])
    pl = convert_raw(raw_status)

    if "plot_24hours" in config:
        for name in config["plot_24hours"]:
            print("Plotting " + name)
            try:
                pl[name].fold_24hours()
                pl[name].plot_folded("time24hf", 24*60, "status", title=name)
            except KeyError:
                print("Character not found!")



