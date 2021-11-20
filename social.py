#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 10:56:43 2021

@author: planetmaker
"""

import pandas as pd
import numpy as np
import scipy as sp

# The logfile is expected to be a csv file in the following format:
# "id","name","status","created_at"
# "1","name1","offline","1632158674"
# "2", "name2","online","1632158679"
# ...

global config
config = {
    "status_filename": 'example.log',
    "concurrency_jitter": 5,
    "status": {
        "offline": 0,
        "online": 1,
        }
    }

class Character():
    name = ""
    rawlog = {
        "time": [],
        "status": [],
        }
    """
    Contains the data about one character and low-level access
    """

    def __init__(self, name, time, status):
        self.name = name
        self.rawlog["status"] = [status]
        self.rawlog["time"] = [time]

    def append_entry(self, time, status):
        self.rawlog["status"].append(status)
        self.rawlog["time"].append(time)


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

        if name not in characters:
            characters[name] = Character(name, time, status)
        else:
            characters[name].append_entry(time, status)

    return characters


if __name__ == '__main__':
    global personal_log # make available to cmd for individual analysis
    raw_status = read_status(config["status_filename"])
    personal_log = convert_raw(raw_status)



