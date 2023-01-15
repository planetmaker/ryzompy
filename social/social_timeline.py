#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 20:10:34 2023

@author: planetmaker
"""

import pandas as pd
# import warnings
# from datetime import datetime, timedelta
# from social_API import to_numeric_status
from social_types import TimelineColumnType
from social_exceptions import TimelineNoRaw

class Timeline:
    
    def __init__(self, dataframe=None):
        if dataframe is not None:
            self.set_dataframe(dataframe)
        else:
            self.dataframe = pd.DataFrame()
    

    
    def get_dataframe(self):
        """
        Returns
        -------
        pandas dataframe
            the complete dataframe with all columns and rows.

        """
        return self.df
    
    
    
    def set_dataframe(self, dataframe):
        self.df = dataframe
            
    

    
    def get_time_limited(self, mint, maxt):
        """
        Limit the time to values between mint and maxt

        Parameters
        ----------
        mint : datetime
            Earliest time to consider
        maxt : datetime
            Latest time to consider

        Returns
        -------
        The timeline limited to times within the interval [mint,maxt]

        """
        mask = (self.df[TimelineColumnType.TIME] > mint) & (self.df[TimelineColumnType.TIME] < maxt)
        return self.df.loc[mask]
    
    
        
    def get_time_resampled(self, delta_t = 120):
        """

        Parameters
        ----------
        delta_t : TYPE, optional
            DESCRIPTION. Resample the time base to equidistant spacing
            Default spacing is 120s

        Returns
        -------
        Resampled timeline

        """
        newdf = self.df.resample(Timedelta, )
        return newdf
    
    
            
    def add_time_from_raw(self):
        self.df[TimelineColumnType.TIME] = None

        try:
            self.df[TimelineColumnType.TIME] = pd.to_datetime(self.df[TimelineColumnType.RAW], unit='s')
        except:
            raise TimelineNoRaw()


    
    
    def add_weekly_timestamps(self):
        """
        Returns
        -------
        None

        """
        self.df['weekly'] = None

        
        
    def add_daily_timestamps(self):
        """
        Returns
        -------
        None
        """
        self.df['daily'] = None
        

        
    def add_monthly_timestamps(self):
        """
        Returns
        -------
        None
        """
    
    
        
    def plot(self, x=TimelineColumnType.TIME, y=TimelineColumnType.STATUS, kind='scatter'):
        """
        Plot the timeline

        Parameters
        ----------
        x : str, Choose the name of the column for x
            DESCRIPTION. The default is 'time'.
        y : str, Choose the name of the column for y
            DESCRIPTION. The default is 'value'.
        kind : str, Plot tye
            DESCRIPTION. The default is 'scatter'.

        Returns
        -------
        None.

        """
        self.df.plot(x,y,kind)


    
            