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
from social_config import config, guild_allegiance
from social_globals import unixtime_to_timestring

import requests
import xmltodict
from datetime import datetime

global guild_dict

def api_guildname_by_id(id):
    global guild_dict
    # try:
    #     if len(guild_dict) > 0:
    #         pass
    #     else:
    #         raise
    # except:
    data = requests.get(config['ryzom_api']['base'] + config['ryzom_api']['guilds'])
    intermediate = xmltodict.parse(data.text)
    guild_dict = intermediate['guilds']['guild']

        # except:
        #     print("Could not load guilds from API")
        #     return ""

    for guild in guild_dict:
        if int(guild['gid']) == id:
            return guild['name']

    print('Guild ID not found:', id)
    return "Not found"


"""
The logfile 'fight.log' is expected to be a csv file in the following format:
id,op,op_owner,op_owner_id,date,customer,customer_guild,attacking_guild,war_type,phase,created_at,created_by,modified_at,objective,comment
"""

def guild_fights():
    try:
        fightlog = pd.read_csv(config['path']['base'] + config['fightlog_filename'])
    except:
        print("Could not read fightlog file")
        return

    owners = set(fightlog['op_owner_id'].unique())
    outposts = set(fightlog['op'].unique())
    customers = set(fightlog['customer_guild'].unique())
    attackers = set(fightlog['attacking_guild'].unique())
    opguilds = set.union(owners, customers, attackers)

    # Analyse by outpost
    allegiance_count = {
        'Kami': 0,
        'Kara': 0,
        'Maro': 0,
        'Ranger': 0,
        'Unknown': 0,
        }
    for outpost in outposts:
        subset = fightlog[fightlog['op'] == outpost]
        print(outpost, ':')
        for index,fight in subset.iterrows():
            try:
                allegiance = guild_allegiance[fight['customer_guild']][0]
                allegiance_count[allegiance] = allegiance_count[allegiance] + 1
            except:
                allegiance = "Unknown"
                allegiance_count["Unknown"] = allegiance_count["Unknown"] + 1
            print(unixtime_to_timestring(fight['date']), allegiance, api_guildname_by_id(fight['customer_guild']), ':', api_guildname_by_id(fight['op_owner_id']), api_guildname_by_id(fight['attacking_guild']))
        print('')

    print("Summary of customers:")
    for item, value in allegiance_count.items():
        print(item,':', value)