#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 11:29:38 2023

@author: planetmaker
"""

class TimelineLengthMismatch(Exception):
    
    def __init__(self, len1, len2, message="Number of entries in time and data column are different"):
        self.len1 = len1
        self.len2 = len2
        super().__init__(self.message)