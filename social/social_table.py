#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:30:20 2022

@author: planetmaker
"""

import pandas as pd
import datetime

global config

from social_API import Social_API
from character import Character
from social_types import Timebase

try:
    from social_config import config
except:
    pass



class Social_Table():
    """
    master class to contain all data available on the social context
    """

    def __init__(self, from_API = False):
        """
        Initialize the table

        Returns
        -------
        None.

        """
        self.charinfo = pd.DataFrame()
        self.SAPI = Social_API()
        self.filenames = {
            "charinfo": "social_table_charinfo.pkl",
            }

        if from_API:
            print("Reading list of names from API...")
            name_list = self.SAPI.get_name_list()
            self.charinfo = pd.DataFrame([], index=name_list, columns=['num_entries'])
        else:
            print("Trying to read data from pickle...")
            self.read_pickle()


    def help():
        """
        Print some help on usage

        Returns
        -------
        None.

        """
        print("""
              Social table basically does the framework:
                  - store a list of characters
                  - give access to the social API database
                  - save or load the information to file
                  
              read_pickle(self, filename): read from file
              save_pickle(self, filename): save to file
              get_name_table: get the list of names. 
                  Returns a dataframe with the name as index and a character object in the column 'char'
              api_download_name_list()
                  Initialize the characterlist with all available names. No time data yet.
              api_download_Timeline_by_name
                  Download the raw time data from the API and add it as Timeline to the character
              """)


    def read_pickle(self, filenames=None):
        """
        Read the changes Dataframe from a pickle file

        Parameters
        ----------
        filename : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        if filenames == None:
            try:
                filenames = config["social_filenames"]
            except:
                filenames = self.filenames
        self.charinfo = pd.read_pickle(filenames['charinfo'])



    def save_pickle(self, filenames=None):
        """
        Save the changes Dataframe to a pickle file

        Parameters
        ----------
        filename : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        None.

        """
        if filenames == None:
            try:
                filenames = config["social_filenames"]
            except:
                filenames = self.filenames
        self.charinfo.to_pickle(filenames['charinfo'])



    def get_name_table(self):
        """
        Return the list of names and character objects

        Returns
        -------
        List of names with associated character objects

        """
        return self.charinfo
    
    
    
    def get_char(self, name):
        """
        Return one character

        Parameters
        ----------
        name : string
            The name of the character to access
            
        Returns
        -------
        One character

        """
        return self.charinfo['char'][name]



    def api_download_name_list(self):
        """
        Download the list of names from API server

        Returns
        -------
        None.

        """
        name_list = self.SAPI.get_name_list()
        self.charinfo = pd.DataFrame([], index=name_list)
        self.charinfo['char'] = None
        for name in name_list:
            self.charinfo['char'][name] = Character(name)



    def api_download_Timeline_by_name(self, name):
        """
        Add the data by name to the table

        Parameters
        ----------
        name : STRING
            name as present in the social DB

        Returns
        -------
        None.

        """
        try:
            raw = self.SAPI.get_raw_dataframe_by_name(name)
        except:
            print("Download failed for " + name)
            return
        
        if not 'char' in self.charinfo:
            self.charinfo['char'] = None
            
        self.charinfo['char'][name].set_timeline_from_df(Timebase.ORIGINAL, raw)



    def get_character_count(self):
        """
        Get the number of online players from the subset of those where data
        are available

        Parameters
        ----------
        do_plot : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        num : TYPE
            DESCRIPTION.

        """
        return len(self.charinfo)



    def add_crosscorrelation(self, char1, char2, timeline, col_time, col_val,result_col_name):
        """
        Add the cross-correlation value for the chars1 and char2 for the values in col_val,
        at times col_time in timeline. Store the results in result_col_name in the characters

        Parameters
        ----------
        char1 : TYPE
            DESCRIPTION.
        char2 : TYPE
            DESCRIPTION.
        timeline : TYPE
            DESCRIPTION.
        col_time : TYPE
            DESCRIPTION.
        col_val : TYPE
            DESCRIPTION.
        result_col_name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        