#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 19:05:45 2021

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

from datetime import datetime

seconds_per_day = 24 * 60 * 60
seconds_per_week = seconds_per_day * 7

def unixtime_to_timestring(unixtime):
    """

    Parameters
    ----------
    unixtime : INT
        Unix timestamp

    Returns
    -------
    TYPE
        Time formated as string %Y-%m-%d %H:%M:%S.

    """
    return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
