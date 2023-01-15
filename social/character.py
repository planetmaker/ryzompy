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
with socialgraph; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

import math
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import requests
import ast

import datetime

from social_globals import seconds_per_day, seconds_per_week
from social_config import config
from social_types import Civ, Cult, GuildRank, Organisation, Language
from social_timeline import Timeline

class Character:
    """
    Contains the data about one character and low-level access
    """

    def __init__(self, name):
        self.vars = {
            'name': name,
            'guild': None,
            'guildrank': GuildRank.UNKNOWN,
            'civ': Civ.UNKNOWN,
            'language': Language.UNKNOWN,
            'organisation': Organisation.UNKNOWN,
            'cult': Cult.UNKNOWN,
            'twinks': None,
            'timelines': dict(),
            'first_seen': None,
            'last_seen': None,
            'num_entries': None,
            'correlations': dict(),
        }
        self.inferred = dict()


    def get(self, prop):
        return self.vars[prop]
    
    def get_name(self):
        return self.get('name')
    
    def get_guild(self):
        return self.get('guild')
    
    def get_guildrank(self):
        return self.get('guildrank')
    
    def get_civ(self):
        return self.get('civ')
    
    def get_language(self):
        return self.get('language')
    
    def get_organisation(self):
        return self.get('organisation')
    
    def get_cult(self):
        return self.get('cult')
    
    def get_twinks(self):
        return self.get('twinks')
    
    def get_first_seen(self):
        return self.get('first_seen')
    
    def get_last_seen(self):
        return self.get('last_seen')

    def get_num_entries(self):
        return self.get('num_entries')
    
    def set_property(self, prop, value, force=False):
        if prop not in self.vars:
            warnings.warn("Adding new property '{}' to char {}!".format(prop, self.vars['name']))
            self.vars[prop] = value
            return

        if type(self.vars[prop]) in [dict, list]:
            if not force:
                warnings.warn("Trying to set list or dict property '{}' for char {}. Skipping".format(prop, self.vars['name']))
                return
            else:
                warnings.warn("Overwriting list- or dict-type property {} for char {}".format(prop, self.vars['name']))
            
        if type(value) is not type(self.vars[prop]) and self.vars[prop] is not None:
            if not force:
                warnings.warn("Trying to change property type for '{}' for char {}. Skipping".format(prop, self.vars['name']))
                return
            else:
                warnings.warn("Changing property type for '{}' for char {}.".format(prop, self.vars['name']))
            
        self.vars[prop] = value
    
    def set_timeline_from_df(self, name, df):
       self.vars['timelines'][name] = Timeline(dataframe=df)
       
        
    
    def amend__timeline(self, timeline_name, timeline):
        self.vars['timelines'][timeline_name]
        
            
    def __str__(self):
        str = ""
        str += "Character '{}' is {} in guild '{}'".format(self.vars['name'], self.vars['guildrank'], self.vars['guild'])
        str += "\nCiv: {}, Org: {}, Cult: {}".format(self.vars['civ'], self.vars['organisation'], self.vars['cult'])
        str += "\nLanguage: {}, first seen: {}, last seen: {} ({} times)".format(self.vars['language'], self.vars['first_seen'], self.vars['last_seen'], self.vars['num_entries'])
        return str
    
