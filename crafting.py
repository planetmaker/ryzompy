#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 17:33:00 2020

@author: planetmaker
"""

import pandas as pd

data_ammobullet = pd.read_csv('data/DB_AMMOBULLET.csv',sep=';')
data_armorclip = pd.read_csv('data/DB_ARMORCLIP.csv',sep=';')
data_barrel = pd.read_csv('data/DB_BARREL.csv',sep=';')
data_clothes = pd.read_csv('data/DB_CLOTHES.csv',sep=';')
data_explosive = pd.read_csv('data/DB_EXPLOSIVE.csv',sep=';')
data_grip = pd.read_csv('data/DB_GRIP.csv',sep=';')
data_jewel = pd.read_csv('data/DB_JEWEL.csv',sep=';')
data_lining = pd.read_csv('data/DB_LINING.csv',sep=';')
data_point = pd.read_csv('data/DB_POINT.csv',sep=';')
data_stuffing = pd.read_csv('data/DB_STUFFING.csv',sep=';')
data_ammojacket = pd.read_csv('data/DB_AMMOJACKET.csv',sep=';')
data_armorshell = pd.read_csv('data/DB_ARMORSHELL.csv',sep=';')
data_blade = pd.read_csv('data/DB_BLADE.csv',sep=';')
data_counterweight = pd.read_csv('data/DB_COUNTERWEIGHT.csv',sep=';')
data_firingpin = pd.read_csv('data/DB_FIRINGPIN.csv',sep=';')
data_hammer = pd.read_csv('data/DB_HAMMER.csv',sep=';')
data_jewelsetting = pd.read_csv('data/DB_JEWELSETTING.csv',sep=';')
data_magicfocus = pd.read_csv('data/DB_MAGICFOCUS.csv',sep=';')
data_shaft = pd.read_csv('data/DB_SHAFT.csv',sep=';')
data_trigger = pd.read_csv('data/DB_TRIGGER.csv',sep=';')

db_list = {'light armor': ['data_armorclip']}

prop_ammobullet = ['haltbarkeit', 'gewicht', 'schaden', 'geschwindigkeit', 'reichweite']
prop_armorclip  = ['haltbarkeit', 'gewicht', 'eigener-ausweich-malus', 'eigener-abwehr-malus', 'schutzfaktor', 'zerschneideschutz', 'zertruemmerungsschutz', 'durchborhungsschutz']
prop_barrel     = ['haltbarkeit', 'gewicht', 'sapladung', 'geschwindigkeit', 'eigener-ausweich-malus', 'eigener-abwehr-malus', 'gegner-ausweich-malus', 'gegner-abwehr-malus']
prop_clothes    = ['haltbarkeit', 'gewicht', 'eigener-ausweich-malus', 'eigener-abwehr-malus', 'schutzfaktor', 'zerschneideschutz', 'zertruemmerungsschutz', 'durchbohrungsschutz']
prop_explosives = ['haltbarkeit', 'gewicht', 'schaden', 'geschwindigkeit', 'reichweite']
prop_grip       = ['haltbarkeit', 'gewicht', 'sapladung', 'geschwindigkeit', 'eigener-ausweich-malus', 'eigener-abwehr-malus']
prop_jewel      = ['haltbarkeit', 'gewicht', 'saeureschutz', 'kaelteschutz', 'verrottungsschutz', 'feuerschutz', 'schockwellenschutz', 'giftschutz', 'elektroschutz']
prop_lining     = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_point      = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_stuffing   = ['haltbarkeit', 'gewicht', 'eigener-ausweich-malus', 'eigener-abwehr-malus', 'schutzfaktor', 'zerschneideschutz', 'zertruemmerungsschutz', 'durchbohrungsschutz']
prop_ammojacket = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_armorshell = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_blade      = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_counterweight = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_firingpin  = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_hammer     = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_jewelsetting  = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_magicfocus = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_shaft      = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
prop_trigger    = ['Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']

grades = {1: 'basic', 2: 'fine', 3: 'choice', 4: 'excellent', 5: 'supreme'}

db_dict = {
    'armorclip': data_armorclip,
    'lining': data_lining,
    'ammobullet': data_ammobullet,
    'explosives': data_explosive,
    }

def get_db(prop):
    global db_dict
    return db_dict[prop]


# prop_weste = {'cloth': 4, 'ruestungsbindung': 4, 'ruestungswattierung': 1, 'ruestungsfixierung' 1}

weste = []
weste.append(data_armorclip.iloc[50])
weste.append(data_armorclip.iloc[55])
weste.append(data_armorclip.iloc[5])
weste.append(data_armorclip.iloc[250])

item = data_armorclip.iloc[50]

# For reference, see:
# https://app.ryzom.com/app_forum/index.php?page=topic/view/23967/1

def adjust_type1(stats):
    vmax = max(stats)
    avg  = sum(stats) / len(stats)
    delta = vmax - avg

    stretch = 30 / delta
    if stretch > 2:
        stretch = 2
    elif stretch < 1:
        stretch = 1
    
    for index in range(1,len(stats)):
        stats[index] = (starts[index] - avg) * stretch + avg
   
    return stats


def adjust_type2(stats):
    return stats


def adjust_type3(stats):
    vmax = max(stats)
    index = stats.index(vmax)
    stats[index] += 10
    return stats



def adjust_phase2(stats):
    diff = get_delta_factor(stats)
    if diff < 30:
        stats = adjust_type1(stats)
        print("Correction type 1")
    elif diff > 35:
        stats = adjust_type3(stats)
        print("Correction type 3")
    else:
        print("Correction type 2")

    return stats        


def calculate_stats(crafting_item):
    # n = len(crafting_item[0])-9
    stats = crafting_item.sum()
    return stats

# get the average for each value

# get the average A of all values V
# get the difference of the average A from the maximum of V, d = max(v) - A
#   if d < 30: 2.1
#   30 <= d <= 35: no change
#   d > 35: first stat +10

def get_item_mats(item_lists):
    # Create an empty dataframe to match the materials
    first = list(item_lists.keys())[0]
    db = get_db(first)
    stats = pd.DataFrame(columns=db.columns)
    
    # iterate over all materal types and materials
    item_no = 0
    for mat_type, matids in item_list.items():
        db = get_db(mat_type)
        for matid in matids:
            stats.loc[item_no] = db.loc[matid]
            item_no += 1
            
    return stats
        
item_list = {
    'armorclip': [50,52,0,33],
    'lining': [30,30,30,35],
    }

my_list=(50,36,42,50)
 


print(data_jewelsetting)

print(weste)