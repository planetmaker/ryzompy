#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:30:20 2022

@author: planetmaker
"""

import pandas as pd
import datetime
from social_API import Social_API
from character import Character

class Social_Table():
    """
    master class to contain all data available on the social context
    """

    def __init__(self, from_API = True):
        """
        Initialize the table

        Returns
        -------
        None.

        """
        self.changes = pd.DataFrame(columns=['id', 'time', 'name', 'status'])
        self.charinfo = pd.DataFrame(columns=['name', 'num_entries', 'char'])
        self.timeinfo = pd.DataFrame()
        self.SAPI = Social_API()
        if from_API:
            name_list = self.SAPI.get_name_list()
            self.charinfo = pd.DataFrame([], index=name_list, columns=['num_entries', 'char'])
            self.timeinfo = pd.DataFrame([])
        else:
            print("Reading from csv currently not implemented!\nName list not populated.")
        self.filename = "social_table.pkl"

    def read_pickle(self, filename=""):
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
        if filename == "":
            try:
                filename = config["status_filename"]
            except:
                filename = self.filename
        self.changes = pd.read_pickle(filename)



    def save_pickle(self, filename=""):
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
        if filename == "":
            try:
                filename = config["status_filename"]
            except:
                filename = self.filename
        self.changes.to_pickle(filename)

    def get_name_table(self):
        """
        Return the list of names and character objects

        Returns
        -------
        List of names with associated character objects

        """
        return self.charinfo

    def get_changes_table(self):
        """
        Return the whole dataframe unabridged

        Returns
        -------
        dataframe with columns 'id', 'time', 'name' and 'status'.

        """
        return self.changes

    def get_time_table(self):
        """
        Return the time table

        Returns
        -------
        dataframe with status times of all characters

        """
        return self.timeinfo

    def api_download_name(self, name):
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
        name_data = self.SAPI.get_status_change_by_name(name)
        if name_data == None:
            return
        df = pd.DataFrame(name_data)
        df.rename(columns={"created_at": "time"}, inplace = True)
        try:
            self.changes = pd.concat([self.changes, df])
        except:
            print("Cannot merge data for ", name)
            print(df)

        self.charinfo['num_entries'][name]  = len(name_data)
        try:
            self.charinfo['char'][name] = Character(name, df[['time','status']])
            # Add data to global time table
            df['status'].replace({'online':1, 'offline':0, '':pd.NA}, inplace=True)
            df.rename(columns={'status': name}, inplace = True)
            df['time'] = [datetime.datetime.fromtimestamp(t) for t in df['time']]
            df.set_index('time', inplace=True)
            print(df)
            self.timeinfo = self.timeinfo.combine_first(df)
        except KeyError as e:
            print("Error adding char data for ", name)
            print(e)
            print(df)
        # except:
        #     print("Unknown error for ", name)
        #     print(df)


    def api_download_names(self, names):
        """
        Add the data by name(s) to the table

        Parameters
        ----------
        names : STRING or list of STRING
            A name or a list of names.

        Returns
        -------
        None.

        """
        if type(names) == 'str':
            self.api_download_name(names)
        elif (type(names) == 'list' or type(names) == 'set'):
            for name in names:
                self.api_download_name(name)
        else:
            print("Unsupported type for 'names'!")

