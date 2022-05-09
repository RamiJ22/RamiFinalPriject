# -*- coding: utf-8 -*-
"""
Created on Sun May  1 19:57:09 2022

@author: Rami
"""
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

import csv

import numpy as np

import seaborn as sns

import requests 
contrib = pd.read_excel("HAL.XLS", dtype=str)
#Replaces 1990s data with 1900 data
contrib['Year'] = contrib['Year'].replace("1900s", "1900")

counts = contrib.groupby("State").size()
#.Size counts the records in each group
Byyear = contrib.groupby(["Year", "State"]).size()

print(contrib["Victim"] +"  " + contrib["Race"])

Statemap = gpd.read_file("cb_2020_us_county_500k.zip")
pop = pd.read_csv("pop.csv", dtype={"GEOID":str})
pop = pop[["GEOID","B02001_003E"]]


Black = pd.read_csv("Black_AL.csv")
joined = gpd.GeoDataFrame(Black.merge(Statemap, on="NAME"))
joined = joined.merge(pop,on = "GEOID", indicator = True, how = "outer")
print(joined["_merge"].value_counts())
joined = joined.drop(columns = "_merge")
joined["VoterRate"] = 100*joined["Black"]/joined["B02001_003E"]
joined["Lynchings"] = contrib

fig2, ax2 = plt.subplots(dpi=300)
fig2.suptitle("Lynchings by County Vs. Black Registration")
plt.scatter(joined["VoterRate"], counts)
plt.show()