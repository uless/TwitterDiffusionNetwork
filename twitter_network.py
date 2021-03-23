#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:43:54 2021

@author: anqi

Things we have not yet considered in this version: 
    Meso users for retweeted quoted tweet
    
"""

#Import packages
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

#%%
#Step 0: pretend we have some data here
follow_dict = {                           #key = user, value = followee
        "1":["3","4","5","6","7"],
        "2":["3","5"],
        "3":["1","4","5","6"],
        "4":["1","2","6","7"],
        "5":["6"],
        "6":["7"],
        "7":["1","2","3","4"]
        }

rt = {
     "Name": ["1","2","3","4","4","5","6","7"],                    #user
     "UltimaID":["001","002","003","004","014","005","006","123"], #ultima_tweet_id
     "SeedID":["123","123","123","123","233","123","123","123"],   #seed_tweet_id
     "Type":["rt","rt","rt","rt","t","rt","rt","t"],               #type
     "Time":[21,20,18,16,17,19,17,15]                              #timestamp
     }

#Need to add: meso data

retweet_df = pd.DataFrame(rt)  

#%%
#Step 1: Find parents
def find_parents (Name, UltimaID, SeedID):
    #find followee double match
    followee_list = follow_dict.get(Name)
    followee_match = retweet_df[(retweet_df.Name.isin(followee_list)) & 
                                (retweet_df["SeedID"] == SeedID)].copy()
    #From time. decide who is responsible for this kid
    kidtime = int(retweet_df.loc[(retweet_df['Name'] == Name) & 
                             (retweet_df["SeedID"] == SeedID) &
                             (retweet_df["UltimaID"] == UltimaID),"Time"])
    followee_match["Gap"] = followee_match["Time"] - kidtime
    near_zero = followee_match.loc[followee_match['Gap'] < 0, 'Gap'].max()
    parent = followee_match.loc[followee_match['Gap'] == near_zero,"UltimaID"].to_string(index=False).strip()
    kid = UltimaID
    return (parent,kid)

#%%
#Step 2: Build tree
family_list = []
for i in range(0,len(retweet_df)-1):
    if retweet_df.loc[i,'Type'] == "rt":
        Name = retweet_df.loc[i,'Name']
        UltimaID = retweet_df.loc[i,'UltimaID']
        SeedID = retweet_df.loc[i,'SeedID']
        kinship = find_parents(Name, UltimaID, SeedID)
        family_list.append(kinship)

tree = nx.DiGraph(family_list)
                
nx.draw(tree)
plt.show()
