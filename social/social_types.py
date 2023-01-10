#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 18:28:47 2022

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


from enum import Enum


# Races as defined in Ryzom
class Civ(Enum):
    UNKNOWN = 0
    TRYKER  = 1
    MATIS   = 2
    FYROS   = 3
    ZORAI   = 4
    
    
class Cult(Enum):
    UNKNOWN  = 0
    NONE     = 1
    KARAVAN  = 2
    KAMI     = 3
    
    
class Organisation(Enum):
    UNKNOWN  = 0
    NONE     = 1
    RANGER   = 2
    MARAUDER = 3


class GuildRank(Enum):
    UNKNOWN     = 0
    MEMBER      = 1
    OFFICER     = 2
    HIGHOFFICER = 3
    LEADER      = 4
    
    
class Language(Enum):
    UNKNOWN = 0
    DE      = 1
    EN      = 2
    ES      = 3
    FR      = 4
    RU      = 5
    