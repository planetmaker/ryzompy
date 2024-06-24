#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 16:03:10 2024

@author:
"""

initial_chest_levels = [10,10,3,2,1, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]
max_chest_level = 10
cost_not_available = 5000000000
max_chests = len(initial_chest_levels)
start_levels = sum(initial_chest_levels)
max_cost = 138+38+30
results = []
max_guildpoints_per_month = 38

# class my_chest():
#     level: 1
#     cum_cost: 0
    
#     def __init__(self, num = None):
#         self.level = 1
#         self.cum_cost = 0
#         if num < 2:
#             self.level = 10
            
#     def get_cum_cost(self):
#         return self.cum_cost
    
#     def get_level(self):
#         return self.level
    
#     def set_level(self, level):
#         self.level = level
        
#     def set_cum_cost(self, cum_cost):
#         self.cum_cost = cum_cost
    
#     def level_up(self): 
#         if self.level < max_chest_level:
#             return cost_not_available
#         self.level += 1
#         cost = self.level ** 2
#         self.cum_cost += cost
#         return cost

# class my_chests():
#     chests: []
#     cum_chest_costs: 0
    
#     def __init__(self, chests = [], cum_chest_costs = 0):
#         self.chests = chests
#         self.chest_costs = cum_chest_costs
        
#     def get_num_chests(self):
#         return len(self.chests)
    
#     def can_add_chest(self):
#         if self.get_num_chests() == max_chests:
#             return False
#         return True
    
#     def create(self):
#         num_chests = self.get_num_chests
#         if self.can_add_chest():
#             self.chests.append(my_chest(num_chests+1))
#         if num_chests > 2:
#             self.chest_costs += (num_chests+1) ** 2
            
#     def level_up(self, chest):
#         if self.get_num_chests() < chest:
#             return
#         self.chests[chest].level_up()
            
           
    

def cost_chest_levelupgrade(n):
    if n == 1:
        return 0
    if n > max_chest_level:
        return cost_not_available
    return n**2

def cost_chest_buy(n):
    if n < 2:
        return 0
    if n > max_chests:
        return cost_not_available
    return n**2

def total_levels(chest_levels):
    return(sum(chest_levels))

def get_number_of_chests(chest_levels):
    chest = 0
    while chest < max_chests:
        if chest_levels[chest] == 0:
            return chest
        chest = chest + 1
    return max_chests

def get_chest_level(chest, chests):
    return chests[chest-1]

def upgrade_chest(chest, chests):
    new_level = get_chest_level(chest,chests) + 1
    chests[chest-1] = new_level
    return(chests)

def walk_tree(cost, levels, chests):
    if cost > max_cost:
        return
    num_chests = get_number_of_chests(chests)

    for i in range(1, num_chests):
        upgradecost = cost_chest_levelupgrade(get_chest_level(i, chests)+1)
        if cost+upgradecost < max_cost:
            walk_tree(cost+upgradecost, levels+1, upgrade_chest(i, chests[:]))
        else:
            print("{}, {}: {}".format(cost, levels, chests))
            results.append((cost, levels, chests))

    num_chests = get_number_of_chests(chests)
    upgradecost = cost_chest_buy(num_chests+1)
    if cost+upgradecost < max_cost:
        walk_tree(cost+upgradecost, levels+1, upgrade_chest(num_chests+1, chests[:]))
    else:
        print("{}, {}: {}".format(cost, levels, chests))
        results.append((cost, levels, chests[:]))

def find_optimum_for_size(res):
    min_cost = max_cost
    max_levels = 0
    for item in res:
        if max_levels > item[1]:
            continue
        if max_levels == item[1] and min_cost < item[0]:
            continue
        best = item[2]
        min_cost = item[0]
        max_levels = item[1]
    print("Best build strategy for {} GP:". format(max_cost))
    print(best)
    print("It costs {} GP and buys {} guild hall levels".format(min_cost, max_levels-start_levels))
    print("Starting formation was: {}".format(initial_chest_levels))

walk_tree(0, total_levels(initial_chest_levels), initial_chest_levels)
find_optimum_for_size(results)
