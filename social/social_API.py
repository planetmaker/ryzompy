#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:48:03 2022

@author: planetmaker
"""

import requests
import pandas as pd
import ast
try:
    from social_config import config
except:
    print("Config not found! Using defaults. Access may fail.")
    pass




def to_numeric_status(string_status):
    if string_status in config['status']:
        return config['status'].get(string_status)
                                    
    return pd.NA




class Social_API:
    """
    Contains the data and access methods about the social API
    """

    def __init__(self, cfg = None):
        """
        Initialize the Social_API

        Parameters
        ----------
        config : social_config as nested dict
            It should contain an entry 'social_api' with the following sub-entries:
                'base', 'name_list', and 'name_status_change'

            'base':
                is the main URL, the rest is extensions to the single end points
            'name_list':
                returns a list of all names stored in the DB of the format:
                [ "name1", "name2", ... ]
            'name_status_change':
                List of the format (individual DB entries):
                [ { "id": 332583, "name": "example", "status": "offline", "created_at": 1653079681 },
                  { "id": 332376, "name": "example", "status": "online", "created_at": 1653067760 },
                  ...
                ]

        Returns
        -------
        None.

        """
        if cfg is not None:
            self.url_config = cfg['social_api']
        else:
            try:
                self.url_config = config['social_api']
            except:
                self.url_config = {
                    'base':             'https://example.com',
                    'name_list':        '/json.php',
                    'name_list_change': '/json.php?name=',
                    }

    def get(self, url=''):
        """
        Read from the API with the given URL

        Parameters
        ----------
        url : STRING, optional
            Complete and valid URL for the API. The default is "".

        Returns
        -------
        variable return type
            The return type depends on the type of API URL queried.
            It will be returned as evaluated expression

            It will return None, if the webpage status is not 200.

        """
        if url == '':
            url = self.url_config['base']
        try:
            r = requests.get(url)
        except:
            return None
        if r.status_code != 200:
            return None

        # only try to evaluate the return text when the status is OK.
        return ast.literal_eval(r.text)

    def get_name_list(self):
        """
        Get the list of all names

        Returns
        -------
        List of strings
            A list with all names in the API.

        """
        url = self.url_config['base'] + self.url_config['name_list']
        return self.get(url)

    def get_status_change_by_name(self, name):
        """
        Get all status changes for a given name

        Parameters
        ----------
        name : string
            name in all small caps to amend the URL by in order to query the status
            changes for the given name

        Returns
        -------
        List of dicts
            The returned list contains dicts of the format
            {
                id: entry_id,
                name: name_string,
                status: online|offline|unknown,
                created_at: unix_timestamp
            }

        """
        url = self.url_config['base'] + self.url_config['name_status_change'] + name
        return self.get(url)
    
    def get_raw_timeline_by_name(self, name):
        """

        Parameters
        ----------
        name : string
            The name to get the status changes for.

        Returns
        -------
        dataframe with column 'time' and 'status'.

        """
        raw = pd.json_normalize(self.get_status_change_by_name(name))
        return raw[['created_at', 'status']]
        
        
    
    def get_guild_by_name(self, name):
        raise NotImplementedError(self.get_guild_by_name.__name__ + ": Not yet implemented")
    
    def get_cult_by_name(self, name):
        raise NotImplementedError(self.get_cult_by_name.__name__ + ": Not yet implemented")
    
    def get_organisation_by_name(self, name):
        raise NotImplementedError(self.get_organisation_by_name.__name__ + ": Not yet implemented")
    
    def get_notes_by_name(self, name):
        raise NotImplementedError(self.get_notes_by_name.__name__ + ": Not yet implemented")

    
    def add_note_by_name(self, name, note):
        raise NotImplementedError(self.add_note_by_name.__name__ + ": Not yet implemented")
    
    def set_cult_by_name(self, name, faction):
        raise NotImplementedError(self.set_cult_by_name.__name__ + ": Not yet implemented")
    
    def set_organisation_by_name(self, name, faction):
        raise NotImplementedError(self.set_organisation_by_name.__name__ + ": Not yet implemented")
    
    def set_guild_by_name(self, name, guild):
        raise NotImplementedError(self.set_guild_by_name.__name__ + ": Not yet implemented")

    def get_race_by_name(self, name):
        raise NotImplementedError(self.get_race_by_name.__name__ + ": Not yet implemented")
    
    def get_guildrank_by_name(self, name):
        raise NotImplementedError(self.get_guildrank_by_name.__name__ + ": Not yet implemented")
    
    def get_language_by_name(self, name):
        raise NotImplementedError(self.get_language_by_name.__name__ + ": Not yet implemented")
    
    def get_char_info_by_name(self, name):
        """
        Parameters
        ----------
        name : TYPE
            DESCRIPTION.

        Returns
            dict of charinfo:
                name: string
                race: string
                organisation: string
                cult: string
                guild: string
                guildrank: string
                language: string
        -------
        None.

        """
        pass
    
