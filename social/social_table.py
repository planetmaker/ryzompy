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
import matplotlib.pyplot as plt

global config
from social_config import config

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
        self.filenames = {
            "changes": "social_table_changes.pkl",
            "charinfo": "social_table_charinfo.pkl",
            "timeinfo": "social_table_timeinfo.pkl",
            }



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
        self.changes = pd.read_pickle(filenames['changes'])
        self.charinfo = pd.read_pickle(filenames['charinfo'])
        self.timeinfo = pd.read_pickle(filenames['timeinfo'])



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
        self.changes.to_pickle(filenames['changes'])
        self.charinfo.to_pickle(filenames['charinfo'])
        self.timeinfo.to_pickle(filenames['timeinfo'])



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



    def api_download_name_list(self):
        """
        Download the list of names from API server

        Returns
        -------
        None.

        """
        name_list = self.SAPI.get_name_list()
        self.charinfo = pd.DataFrame([], index=name_list, columns=['num_entries', 'char'])


    def api_download_changes_by_name(self, name):
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
            self.charinfo['num_entries'][name] = 0
            print(df)

        self.charinfo['num_entries'][name]  = len(name_data)
        # Currently the Character class is not needed or used. Disabled to save memory
        # try:
        #     self.charinfo['char'][name] = Character(name, df[['time','status']])
        #     print("Added ",name," to character list.")
        # except KeyError as e:
        #     print("Error adding char data for ", name)
        #     print(e)
        #     print(df)
        # except:
        #     print("Unknown error for ", name)
        #     print(df)

    def create_name_table(self):
        """
        Create or update the charinfo table from the changes table

        Returns
        -------
        None.

        """
        self.changes.drop_duplicates(ignore_index=True, inplace=True)
        # df = pd.DataFrame(columns=['name','num_entries'])
        frames = dict()
        frames = {name: len(self.changes[self.changes['name'].where(self.changes['name'] == name).notna()].index) for name in set(self.changes['name'])}
        print(frames)
        self.charinfo = pd.DataFrame.from_dict(frames, orient='index', columns=['num_entries'])



    def create_time_table(self, min_datapoints = None):
        """
        Create a global table with status for each character and a common time basis

        Parameters
        ----------
        min_datapoints : int, optional
            Minimal number of data points for a character to be inserted in the table
            The default is taken from the config file.

        Returns
        -------
        None.

        """
        # Add data to global time table
        if min_datapoints == None:
            min_datapoints = config['min_datapoints']
        names = list(self.charinfo.loc[(self.charinfo['num_entries'] >= min_datapoints)].index)

        for name in names:
            df = self.changes.loc[(self.changes['name'] == name)][['time','name']]
            try:
                df['status'].replace({'online':1, 'offline':0, '':pd.NA}, inplace=True)
                df.rename(columns={'status': name}, inplace = True)
                df['time'] = [datetime.datetime.fromtimestamp(t) for t in df['time']]
                df.set_index('time', inplace=True)
                self.timeinfo = self.timeinfo.combine_first(df)
                print("Added ",name," to time table.")
            except KeyError as e:
                print("Error adding char data for ", name)
                print(e)
                print(df)
            except:
                print("Unknown error for ", name)
                print(df)



    def get_cdf_login_count(self, do_plot = False):
        """
        Get the distribution function of the number of data points for characters

        Parameters
        ----------
        do_plot : bool, optional
            Whether to plot the distribution functions. The default is False.

        Returns
        -------
        stat_df : DataFrame with the probability (pdf) and cumulative (cdf)
                  distribution functions

        """
        stat_df = pd.DataFrame(self.charinfo['num_entries'].value_counts()).sort_index().rename(columns={'num_entries':'count'})
        stat_df['pdf'] = stat_df['count'] / sum(stat_df['count'])
        stat_df['cdf'] = stat_df['pdf'].cumsum()
        stat_df = stat_df.reset_index()

        if do_plot:
            stat_df.plot.bar(x = 'index', y = ['pdf', 'cdf'], grid = False)

        return stat_df

    def api_download_changes_by_names(self, names, alle=False):
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
        if alle:
            names = list(self.charinfo.index)

        if isinstance(names, str):
            self.api_download_changes_by_name(names)
        elif (isinstance(names, list) or isinstance(names, set)):
            for name in names:
                self.api_download_changes_by_name(name)
        else:
            print("Unsupported type for 'names': ", type(names))



    def sanitize_timetable(self):
        """
        Replace all NaN values by proper numbers

        Returns
        -------
        None.

        """
        # There is an id column... that's spurious.
        try:
            self.timeinfo.drop('id', 1, inplace=True)
        except KeyError:
            pass
        self.timeinfo.fillna(method='ffill', inplace=True)
        self.timeinfo.fillna(value=0, inplace=True)



    def get_character_count(self, do_plot=False):
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
        num = self.timeinfo.sum(axis=1)
        if do_plot:
            plt.plot(num)
        return num



