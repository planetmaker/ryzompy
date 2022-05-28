#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:30:20 2022

@author: planetmaker
"""

import pandas as pd
import social_API

class Social_Table():
    """
    master class to contain all data available on the social context
    """

    def init(self):
        """
        Initialize the table

        Returns
        -------
        None.

        """
        self.changes = pd.DataFrame(columns=['id', 'time', 'name', 'status'])
        self.charinfo = pd.DataFrame(columns=['name', 'num_entries'])

    def get_changes(self):
        """
        Return the whole dataframe unabridged

        Returns
        -------
        dataframe with columns 'id', 'time', 'name' and 'status'.

        """
        return self.changes


    def download_name(self, name):
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
        name_list = social_API.get_status_change_by_name(name)
        if name_list == None:
            return

        for item in name_list:
            self.changes.append({
                'id':       item['id'],
                'time':     item['created_at'],
                'status':   item['status'],
                'name':     item['name'],
                }, ignore_index=True)
        self.charinfo.append({'name':item['name'], 'num_entries': len(name_list)})

    def download_names(self, names):
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
            download_name(names)
        elif type(names) == 'list':
            for name in names:
                download_name(name)


