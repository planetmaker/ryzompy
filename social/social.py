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
import warnings
from datetime import datetime
from matplotlib import pyplot as plt

global config
from social_config import config
from social_table import Social_Table
from character import Character
from social_types import Timebase, TimelineColumnType

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
    "social_api": {
        "base": "https://example.com",
        "name_list": "/name.php",
        "name_status_change": "/name.php?name=",
        }
    "concurrency_jitter": 60,
    "status": {
        "offline": 0,
        "online": 1,
        "unknown": pd.NA,
        },
    "timeframe": {
        "minimum": 1632158674,            # 0 => 1.1.1970, 0:00h (unix time base)
        "maximum": 1653799284,            # like now
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



def has_known_twink(name):
    """
    Returns True when the name is in the list of known twinks as defined
    in the config file

    Parameters
    ----------
    name : string
        name of the character to check

    Returns
    -------
    bool
        Whether the character has twinks.

    """
    for item in config['known_twinks']:
        if name in item:
            return True
    return False


def get_known_twinks(name):
    """
    Return the set of known twinks as defined in the config file

    Parameters
    ----------
    name : string
        The name of the char to return the twinks for

    Returns
    -------
    Set of twink names.

    """
    for item in config['known twinks']:
        if name in item:
            return item
    return set()
    



if __name__ == '__main__':
    global st
    print("Using config:")
    print(config)

    # raw_status = read_status(config["status_filename"])
    st = Social_Table(from_API=config["reinit_from_API"])
    
    # Populate table with all names
    st.api_download_name_list()

    # First get an overview over selected interesting chars
    
    char_set = set(config['interesting_chars'])
    for twinkset in config['known_twinks']:
        char_set = char_set.union(twinkset)
    char_set = char_set.union(set(config['known_distinct']))
    
    for name in char_set:
        print(name + ':')
        try:
            st.api_download_Timeline_by_name(name)
            print(st.get_char(name).get_num_entries())
        except KeyError:
            warnings.warn(name + ' not found in character database')
            continue
        ch = st.get_char(name)
        tl = ch.get('timelines')[Timebase.ORIGINAL]
        
        # add the raw data
        tl.add_time_from_raw()
        
        # Add numeric status
        df = tl.get_dataframe()
        df['num_status'] = pd.NA
        df.loc[df['status'].str.contains("off"), 'num_status'] = 0
        df.loc[df['status'].str.contains("on"), 'num_status'] = 1
        
        # make time the new index
        # TODO: ValueError: cannot reindex a non-unique index with a method or limit
        df.set_index(TimelineColumnType.TIME, drop=False, inplace=True)
        
        # create a 2-minute time series
        try:
            ch.set_timeline_from_df(Timebase.DELTA_120S, df.resample('120S').ffill())
        except ValueError:
            warnings.warn(name + ': Non-unique index. Skipping.')
            continue
        tl120s = ch.get('timelines')[Timebase.DELTA_120S]
        df120s = tl120s.get_dataframe()
        df120s['hour'] = df120s[TimelineColumnType.TIME].dt.hour
        df120s['weekday_hour'] = df120s.index.weekday*24+df120s['hour']
        df120s['week'] = df120s.index.isocalendar().week
        df120s['dayofyear'] = df120s.index.dayofyear
        
        # Create dataset with data only from 2022
        ch.add_timeline('year2022',tl120s.get_time_limited(
            datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), 
            datetime.strptime('2022-12-31 23:59:59', '%Y-%m-%d %H:%M:%S')
            )
            )

        # plot data folded by week
        ch.add_timeline('online_weekfold_hourly', df120s[['num_status','weekday_hour']].groupby(['weekday_hour']).sum())
        ax = df120s['weekday_hour'].plot(bins=7*24, kind='hist', title=name.capitalize(), figure=plt.figure(), xticks=[0,24,48,72,96,120,144,168])
        ax.figure.savefig(config['paths']['plots'] + 'onlinetime_hourly_' + name + '.png')

        # plot some statistics for 2022
        df2022 = (ch.get('timelines')['year2022']).get_dataframe()
        
#        hist = df2022[['num_status','dayofyear']].groupy(['dayofyear']).sum()
#        ch.add_timeline('online_by_dayofyear2022', hist)
#        ch.add_timeline('online_by_dayofyear2022', df2022[['num_status','dayofyear']].groupy(['dayofyear']).sum())
        ax = df2022[['num_status','dayofyear']].groupby(['dayofyear']).sum().plot(title=name.capitalize(),ylabel='daily online time', kind='bar')
        ax.figure.savefig(config['paths']['plots'] + 'onlinetime_dayofyear2022_' + name + '.png')
        
 #       ch.add_timeline('online_by_week', df2022[['num_status','week']].groupby(['week']).sum())
        ax = df2022[['num_status','week']].groupby(['week']).sum().plot(title=name.capitalize(),ylabel='weekly online time',kind='bar')
        ax.figure.savefig(config['paths']['plots'] + 'onlinetime_weekly2022_' + name + '.png')


        # df2022['num_status'].dropna().plot(kind='hist',bins=365, title=name.capitalize(), figure=plt.figure())
        
        
    ch = st.get_char(config['interesting_chars'][0]) 
    tl = ch.get('timelines')[Timebase.ORIGINAL]
    tl120s = ch.get('timelines')[Timebase.DELTA_120S]
    df120s = tl120s.get_dataframe()
    df2022 = ch.get('timelines')['year2022'].get_dataframe()

    # names = set(config['known_distinct']).union(set(config['vino_chars']), set(config['known_leaders']))
    # for item in config['known_twinks']:
    #     names = names.union(set(item))
    # print("Using names: ", names)

    # for name in names:
    #     st.api_download_changes_by_name(name)
    # st.api_download_names(names)


    # if "plot_24hours" in config:
    #     for name in config["plot_24hours"]:
    #         print("Plotting " + name)
    #         try:
    #             pl[name].fold_24hours()
    #             pl[name].plot_folded("time24hf", 24*60, "status", title=name)
    #         except KeyError:
    #             print("Character not found!")

# st = Social_Table()
# st.api_download_changes_by_names("", alle=True)
# lt = st.get_logentries_table()
# lt['realtimes'] = [datetime.datetime.fromtimestamp(t) for t in lt['time']]

