#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 04 15:30:00 2022

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

global config

from social_config import config
from social_table import Social_Table

st = Social_Table()


"""
class Social_table:
    rawlog:
        id, timestamp, name, status
        
    name_list:
        [name1, name2, ...]
        
    
class Character:
    name: string
    first_seen: datetime
    last_seen: datetime
    flags: Flags
    twinks: [(name: string, auto: bool, date: datetime)]
    comments: [string]
    guild: [(name: string, time: datetime)]
    civ: Race
    organisation: Organisation
    cult: Cult
    guild_rank: Rank
    language: Language
    data: [Time_series]
    
class Race
    Unknown, Tryker, Matis, Fyros, Zorai 
class Organisation
    Unknown, None, Ranger, Marauder
class Cult
    Unknown, Karavan, Kami
class Flags
    AutoTwink, ManualTwink, AutoGuild, ManualGuild, AutoCult, ManualCullt, AutoCiv, ManualCiv
class Rank
    Unknown, Member, Officer, HighOfficer, Leader

class Time_series
    name: string
    data = pd.Series
    time: [datetime]
    values: [int]
    

class Guild
    name: string
    createion_date: datetime
    iconID: int
    
    
"""