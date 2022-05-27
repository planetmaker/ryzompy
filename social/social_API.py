#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:48:03 2022

@author: planetmaker
"""

import requests
import ast

class Social_API:
    """
    Contains the data and access methods about the social API
    """

    def __init__(self, config):
        """
        Initialize the Social_API

        Parameters
        ----------
        config : social_config as nested dict
            It should contain an entry 'social_api' with the following sub-entries:
                'base', 'name_list', and 'name_status_change'

        Returns
        -------
        None.

        """
        self.url_config = config['social_api']

    def get(self, url=""):
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
        if url == "":
            url = self.url_config['base']
        try:
            r = requests.get(url)
        except:
            pass
        if r.status_code is not 200:
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
        return self.get(url=self.url_config['base'] + self.url_config['name_list'])

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

