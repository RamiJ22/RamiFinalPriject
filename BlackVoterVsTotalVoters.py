# -*- coding: utf-8 -*-
"""
Created on Sun May  1 17:35:53 2022

@author: Rami
"""

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

import csv

import numpy as np

import seaborn as sns

import requests
#Filters the states down the ones with lynchings
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

#%%

fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("Black Voter Rate By County")
joined.plot("VoterRate", ax = ax1, legend = True)
ax1.axis("off")
fig.savefig('StatemapAL.png')

#Consider plotting voter registration rate and then draw a map of lynchings next to it
#Then draw a scatterplot has lynchings on one axis and voter registration on the second
# I'll play around with that


#  Read a file of spelling corrections

fixup = pd.read_csv('fixup.csv')
fixup = fixup.dropna(subset='fix_name')

Database = pd.read_excel("ALVR-2022.xlsx", dtype=str)
Database["Active"] = Database["Active"].str.strip()

Database2 = pd.read_excel("ALVR-2022.xlsx", dtype=str)

sns.heatmap(Statemap)