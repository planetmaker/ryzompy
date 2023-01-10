#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 23:06:54 2021

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

from social_config import config

def similar(value1, value2, delta=config["concurrency_jitter"], direction=0):
    """
    Parameters
    ----------
    value1 : TYPE
        DESCRIPTION.
    value2 : TYPE
        DESCRIPTION.
    delta : int, optional
        time difference to consider acceptable. The default is config["concurrency_jitter"].
    direction : int, optional
        directionality of comparison.
         0  : assume no directionality, -delta < v1 - v2 < delta
         1  : only check whether value2 follows value1 within delta. -delta < v1 - v2 < 0
        -1  : only check whether value2 preceeds value1 within delta. 0 < v1 - v2 < delta
    Returns
    -------
    bool
        Whether values agree within delta.

    """
    minv = -delta if direction != -1 else 0
    maxv = delta if direction != 1 else 0
    return minv < value1 - value2 < maxv

# TODO:

# convert timestamp to timedate
# convert timedate to timestamp
# 