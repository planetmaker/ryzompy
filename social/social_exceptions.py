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
        self.message = message
        super().__init__(self.message)
        
class TimelineNoRaw(Exception):
    def __init__(self, char=None, timeline=None):
        self.char = '(unknown)'
        self.timeline ='(unknown)'
        
        if char is not None:
            self.char = char
        if timeline is not None:
            self.timeline = timeline
            
        self.message = "No raw timestamp entry found for char {} in timeline {}".format(self.char, self.timeline)
            
        super().__init__(self.message)