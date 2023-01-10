#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:30:20 2022

@author: planetmaker
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt

global config
from social_API import Social_API
from social_config import config
from character import Character

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
            raw = self.SAPI.get_raw_timeline_by_name(name)
        except:
            print("Download failed for " + name)
            return
        
        if not 'char' in self.charinfo:
            self.charinfo['char'] = None
            
        self.charinfo['char'][name].update_timeline({ 'name': 'tl_raw', 'data': raw})



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



