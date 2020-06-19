#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:42:50 2020

@author: planetmaker
"""

import json
import pandas as pd

def read_json_file(filename):
    with open(filename) as file:
        data = json.load(file)
    return data


def read_data():
    craftplans = read_json_file('json/crafplan.json')
    words_item = read_json_file('json/words_de_item.json')
    words_sbrick = read_json_file('json/words_de_sbrick.json')
    items = read_json_file('json/items.json')
    resources = read_json_file('json/resource_stats.json')

def get_resource_table():
    resources = read_json_file('json/resource_stats.json')

def get_item_property_translation(cryt):
    """
    Parameters
    ----------
    cryt : string
        the cryptic name of a material property like 'armour fixation'
        used in the json files
    Returns
    -------
    clear : string
        the readable property type of the material

    """
    # TODO get the actual meaning of these cryptic strings
    values = {
            "mpftMpAT": "mpftMpAT",
            "mpftMpBT": "mpftMpBT",
            "mpftMpC":  "mpftMpC",
            "mpftMpCA": "mpftMpCA",
            "mpftMpCF": "mpftMpCF",
            "mpftMpCR": "mpftMpCR",
            "mpftMpE":  "mpftMpE",
            "mpftMpED": "mpftMpED",
            "mpftMpEN": "mpftMpEN",
            "mpftMpG":  "mpftMpG",
            "mpftMpGA": "mpftMpGA",
            "mpftMpH":  "mpftMpH",
            "mpftMpJH": "mpftMpJH",
            "mpftMpL":  "mpftMpL",
            "mpftMpM":  "mpftMpM",
            "mpftMpMF": "mpftMpMF",
            "mpftMpP":  "mpftMpP",
            "mpftMpPE": "mpftMpPE",
            "mpftMpPES":"mpftMpPES",
            "mpftMpPR": "mpftMpPR",
            "mpftMpRE": "mpftMpRE",
            "mpftMpRI": "mpftMpRI",
            "mpftMpSH": "mpftMpSH",
            "mpftMpSU": "mpftMpSU",
            "mpftMpTK": "mpftMpTK",
            "mpftMpVE": "mpftMpVE",
            }

    return values[crypt]

def get_ecosystem_from_number(num):
    values = {
        0: 'None',
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',
        6: 'Urwurzeln',
        }
    try:
        ret = values[num]
    except:
        ret = None
    return ret

def get_colour_from_number(num):
    colour_str = ""
    return colour_str

class names():
    def __init__(self):
        pass

class items():

    j_items = dict()

    def __init__(self):
        self.j_items = read_json_file('json/items.json')
        # _items = pd.DataFrame.from_dict(j_items)

    def get_by_id(self, id):
        try:
            return self.j_items[id]
        except:
            return None



class crafting_plans():
    """
    Methods related to the treatment of the crafting plans
    """

    plans = None

    def __init__(self):
        """
        Initialize the crafting plan array from the files and
        convert it into an easier-to-use pandas table
        Returns
        -------
        None.

        """
        j_plans = read_json_file('json/craftplan.json')
        self.plans = dict()
        # num = 0
        for plan,item in j_plans.items():
            try:
                stats = item['mpft']
                stats['plan'] = plan
                stats['item_type'] = item['item_type']
                stats['name'] = ""

                if len(self.plans) == 0:
                    self.plans = pd.DataFrame({k: [v] for k,v in stats.items()})
                else:
                    self.plans = self.plans.append({k: v for k,v in stats.items()}, ignore_index=True)
            except:
                print('Error on ',plan, ': ', item)
                pass

    def get_by_id(self, id):
        try:
            return self.plans[id]
        except:
            print('Plan not found: ', id)
            return None

    def get_all(self):
        return self.plans

    def get_list(self):
        l = list()
        for name,prop in self.plans.items():
            l.append(name)
        return l


class resources():
    """
    Methods related to  treatment of the ressource stats
    """

    ress = dict()

    def __init__(self, items):
        """
        Initialize the ressource info array from the files and
        convert it into an easier-to-use pandas table
        Returns
        -------
        None.

        """
        j_ress = read_json_file('json/resource_stats.json')
        self.ress = dict()
        # num = 0
        for material,item in j_ress.items():
            mat_stats = items.get_by_id(material)
            if mat_stats is None:
                print('No stats found for material: ', material)
                continue
            # num += 1
            # if num > 50:
            #     return
            for prop,stats in item['stats'].items():
                stats['material'] = material
                stats = {**stats, **mat_stats}
                if prop in self.ress:
                    self.ress[prop] = self.ress[prop].append({k: v for k,v in stats.items()}, ignore_index=True)
                else:
                    self.ress[prop] = pd.DataFrame({k: [v] for k,v in stats.items()})

    def get_materials(self, prop):
        # return self.mpftMpAT
        try:
            return self.ress[prop]
        except:
            return None

    def get_all(self):
        return self.ress

    def get_material_properties(self, material, usage):
        try:
            usage_mats = self.ress[usage]
            return usage_mats[usage_mats['material'] == material]
        except:
            print('Material not found in usage:', material, usage_mats)
            return None
