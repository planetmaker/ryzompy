#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 20:10:34 2023

@author: planetmaker
"""

import pandas as pd
import warnings
from datetime import datetime, timedelta
from social_API import to_numeric_status

class Timeline:
    
    def __init__(self, dataframe=None):
        if dataframe is not None:
            self.set_df(dataframe)
        else:
            self.df = pd.DataFrame()
    

    
    def get_df(self):
        return self.df
    
    
    
    def set_df(self, dataframe):
        self.df = dataframe
            
    
    def time_resample(self, delta_t = 120):
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
        newdf = self.df.resample()
        return newdf

    
    
class BaseTimeline(Timeline):
    def __init__(self, raw=None):
        super().__init__()
        if raw is not None:
            df = self.convert_from_raw(raw)
            self.set_df(df)


            
    def convert_from_raw(self, raw):
        df = raw
        df['time'] = None
        df['value'] = None
        try:
            df['time'] = pd.to_datetime(raw['created_at'], unit='s')
        except:
            warnings.warn("No column 'time' found")
        try:
            df['value'] = to_numeric_status(raw['status'])
        except:
            warnings.warn("No column 'status' found")
            
        return df


    
    def limit_time(self, mint, maxt):
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
        raise NotImplementedError()
        return self.df

    
    
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
    
    
        
    def plot(self, x='time', y='value', kind='scatter'):
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
            