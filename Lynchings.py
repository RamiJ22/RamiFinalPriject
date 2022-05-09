# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:30:10 2022

@author: Rami
"""

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

import csv

import numpy as np

import seaborn as sns

import requests 

#  Count lynchings

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

pop = pd.read_csv("pop.csv", dtype={"GEOID":str})
pop = pop[["GEOID","B02001_003E"]]
joined.plot(column="Black", cmap="OrRd")
joined = joined.merge(pop,on = "GEOID", indicator = True, how = "outer")
print(joined["_merge"].value_counts())
joined = joined.drop(columns = "_merge")
joined["VoterRate"] = 100*joined["Black"]/joined["B02001_003E"]

Database = pd.read_excel("HAL.XLS", dtype=str)
Database["County"] = Database["County"].str.strip()

fixup = pd.read_csv('fixup.csv')
fixup = fixup.dropna(subset='fix_name')

Database = Database.query("County != 'Indeterminant'")
Database = Database.query("County != 'Undetermined'")

Database = Database.merge(fixup,on=['State','County'],how='left')
no_fix = Database['fix_name'].isna()
Database['County'] = Database['County'].where(no_fix,Database['fix_name'])
Database = Database.drop(columns='fix_name')
##Adds data from db_counties to joined. Merging them.
db_counties = Database.groupby(["State", "County"]).size()
db_counties = db_counties.reset_index()
db_counties = db_counties.rename(columns = {0:"lynchings"})

db_counties = db_counties.query("State == 'AL'")


db_counties = db_counties[["County","lynchings"]]

joined = joined.merge(db_counties, left_on = "NAME", right_on = "County", indicator = True, how = "outer")
print(joined["_merge"].value_counts())
joined = joined.drop(columns = "_merge")

joined["lynchrate"] = 100*joined["lynchings"]/joined["B02001_003E"]
#%%
fig2, ax2 = plt.subplots(dpi=300) 
fig2.suptitle("Lynchings by County Vs. Black Voter Registration Rate")
joined.plot.scatter(x = "lynchings", y ="VoterRate", ax = ax2)
ax2.set_xlabel("Lynchings")
ax2.set_ylabel("Black Voter Registration Rate")

fig2.tight_layout()

fig2.savefig("AL Lynchings Chart.png")
#%%
plt.rcParams["figure.dpi"] = 300
fg = sns.lmplot(data = joined, x = "lynchings", y = "VoterRate")
fg.set_axis_labels("Lynchings", "Black Voter Registration Rate in AL")
fg.figure.suptitle("The Impact of Lynchings on Black Voter Registration")
fg.figure.tight_layout()
fg.savefig("AL Lynchings Regression.png")