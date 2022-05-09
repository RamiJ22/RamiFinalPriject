# -*- coding: utf-8 -*-
"""
Created on Sun May  1 18:13:54 2022

@author: Rami
"""

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

import csv

import numpy as np

import seaborn as sns

import requests 
Statemap = gpd.read_file("cb_2020_us_county_500k.zip")
#States in this list - AL - TN
States = ["01"] 
Statemap = Statemap[ Statemap['STATEFP'].isin(States)]

#Writes geopackage file
Statemap.to_file("StatemapAL.gpkg", layer = "counties", index=False)
####
Statemap.to_csv("StateMAP1.csv")
Black = pd.read_csv("Black_AL.csv")
joined = gpd.GeoDataFrame(Black.merge(Statemap, on="NAME"))
joined.to_file("StatemapAL.gpkg", layer = "counties", index=False)
joined.plot(column="Black", cmap="OrRd")
joined.to_file("StatemapALBlack.gpkg", layer = "NAME", index=False)
joined.to_file("StatemapALBlack1.gpkg", layer = "Black", index=False)

pop = pd.read_csv("pop.csv", dtype={"GEOID":str})
pop = pop[["GEOID","B02001_003E"]]
joined = joined.merge(pop,on = "GEOID", indicator = True, how = "outer")
print(joined["_merge"].value_counts())
joined = joined.drop(columns = "_merge")
joined["VoterRate"] = 100*joined["Black"]/joined["B02001_003E"]

contrib = pd.read_excel("HAL.XLS", dtype=str)
#Replaces 1990s data with 1900 data
contrib['Year'] = contrib['Year'].replace("1900s", "1900")

print(contrib["Victim"] +"  " + contrib["Race"])

Lynch_cand = contrib["State"]

#Groups by state
counts = contrib.groupby("State").size()
#.Size counts the records in each group
Byyear = contrib.groupby(["Year", "State"]).size()
#Gives you one column per state
Byyear = Byyear.unstack()
fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("Lynchings by State from 1882 - 1930")


counts.plot.bar(ax=ax1, fontsize=7)
#Labels
#ax1.set_ylabel("Year")
ax1.set_xlabel("State")

fig2, ax2 = plt.subplots(dpi=300)
fig2.suptitle("Voter registration by county")
Byyear.plot.area(ax = ax2, fontsize = 7, stacked = True)

price = joined["NAME"]
sales_per_day = joined["VoterRate"]

plt.scatter(price, sales_per_day)
plt.show()