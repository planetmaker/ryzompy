#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:30:20 2022

@author: planetmaker
"""

import pandas as pd
import datetime
from social_API import Social_API
import matplotlib.pyplot as plt

global config
from social_config import config

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
        self.logentries = pd.DataFrame(columns=['id', 'time', 'name', 'status'])
        self.charinfo = pd.DataFrame(columns=['name', 'num_entries'])
        self.timeinfo = pd.DataFrame()
        self.SAPI = Social_API()
        self.time_log_array = []
        self.timeinfo = pd.SparseDtype(("int", 0))
        self.filenames = {
            "changes": "social_table_changes.pkl",
            "charinfo": "social_table_charinfo.pkl",
            "timeinfo": "social_table_timeinfo.pkl",
            }

        if from_API:
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
        self.logentries = pd.read_pickle(filenames['changes'])
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
        self.logentries.to_pickle(filenames['changes'])
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



    def round_timestamps(self, deltat=None):
        """
        Add time column 't' rounded to the jitter time defined in the config or specified

        Parameters
        ----------
        deltat : TYPE, time in seconds
            time to round to. The default is concurrency_jitter from config.

        Returns
        -------
        None.

        """
        if deltat == None:
            deltat = str(config['concurrency_jitter']) + 's'

        self.logentries['t'] = pd.DataFrame([pd.Timestamp.fromtimestamp(t) for t in self.logentries['time']],columns=['t'])['t'].dt.round(deltat)



    def get_logentries_table(self):
        """
        Return the whole dataframe unabridged

        Returns
        -------
        dataframe with columns 'id', 'time', 'name' and 'status'.

        """
        return self.logentries



    def calc_concurrency_for_name(self, name, force_check = False):
        """
        Find the

        Parameters
        ----------
        name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if 'on_on' not in self.charinfo.columns:
            self.charinfo['on_on'] = pd.NaT
        if 'off_off' not in self.charinfo.columns:
            self.charinfo['off_off'] = pd.NaT
        if 'on_off' not in self.charinfo.columns:
            self.charinfo['on_off'] = pd.NaT
        dfname = self.logentries[self.logentries['name'] == name]

        for time,ownstatus in zip(dfname['t'],dfname['status']):
            dft = self.logentries[self.logentries['t'] == time]
            for othername,status in zip(dft['name'],dft['status']):
                # Make sure we populate the matrix for both chars concurrently to avoid double analysis
                if (othername not in self.charinfo[name]['on_on'] and othername not in self.charinfo[name]['off_off'] and othername not in self.charinfo[name]['on_off']) or force_check:
                    if ownstatus == 'online' and status == 'online':
                        try:
                            self.charinfo[name]['on_on'][othername] = self.charinfo[name]['on_on'][othername] + 1
                            self.charinfo[othername]['on_on'][name] = self.charinfo[othername]['on_on'][name] + 1
                        except:
                            self.charinfo[name]['on_on'][othername] = 1
                            self.charinfo[othername]['on_on'][name] = 1

                    elif ownstatus == 'offline' and status == 'offline':
                        try:
                            self.charinfo[name]['off_off'][othername] = self.charinfo[name]['off_off'][othername] + 1
                            self.charinfo[othername]['off_off'][name] = self.charinfo[othername]['off_off'][name] + 1
                        except:
                            self.charinfo[name]['off_off'][othername] = 1
                            self.charinfo[othername]['off_off'][name] = 1
                    else:
                        try:
                            self.charinfo[name]['on_off'][othername] = self.charinfo[name]['on_off'][othername] + 1
                            self.charinfo[othername]['on_off'][name] = self.charinfo[othername]['on_off'][name] + 1
                        except:
                            self.charinfo[name]['on_off'][othername] = 1
                            self.charinfo[othername]['on_off'][name] = 1



    def get_concurrent_status_change(self, name, change, limit=None):
        """
        Get the number of one concurrent status change of the given name wrt
        to all other chars

        Parameters
        ----------
        name : string
            Name of the character to query
        change : string
            'on_on', 'off_off', 'on_off'
        limit : int, optional
            Number of entries to return, highest first. The default is None.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.charinfo[name][change]



    def get_concurrent_status_changes(self, name, limit=None):
        """
        Get the number concurrent status changes (all types) of the given
        name wrt to all other chars

        Parameters
        ----------
        name : string
            Name of the character to query
        limit : int, optional
            Number of entries to return, highest first. The default is None.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return (self.get_concurrent_status_change(name, 'on_on', limit),
                self.get_concurrent_status_change(name, 'off_off', limit),
                self.get_concurrent_status_change(name, 'on_off', limit))



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
        self.charinfo = pd.DataFrame([], index=name_list, columns=['num_entries'])


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
            self.logentries = pd.concat([self.logentries, df])
        except:
            print("Cannot merge data for ", name)
            self.charinfo['num_entries'][name] = 0
            print(df)

        self.charinfo['num_entries'][name]  = len(name_data)



    def create_name_table(self):
        """
        Create or update the charinfo table from the changes table

        Returns
        -------
        None.

        """
        self.logentries.drop_duplicates(ignore_index=True, inplace=True)
        # df = pd.DataFrame(columns=['name','num_entries'])
        frames = dict()
        frames = {name: len(self.logentries[self.logentries['name'].where(self.logentries['name'] == name).notna()].index) for name in set(self.logentries['name'])}
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
            df = self.logentries.loc[(self.logentries['name'] == name)][['time','status']]
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
        self.time_log_array = list(self.logentries['time'].unique())



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



