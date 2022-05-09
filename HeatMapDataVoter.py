# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 13:13:45 2022

@author: Rami
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:34:32 2022

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


####

fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("States")
Statemap.plot(ax=ax1)
ax1.axis("off")
fig.savefig('StatemapAL.png')




#  Read a file of spelling corrections

fixup = pd.read_csv('fixup.csv')
fixup = fixup.dropna(subset='fix_name')

Database = pd.read_excel("ALVR-2022.xlsx", dtype=str)
Database["Active"] = Database["Active"].str.strip()

Database2 = pd.read_excel("ALVR-2022.xlsx", dtype=str)

sns.heatmap(Statemap)

#  Remove entries with unknown counties

Database = Database.query("County != 'Indeterminant'")
Database = Database.query("County != 'Undetermined'")

#  Correct misspellings

Database = Database.merge(fixup,on=['State','County'],how='left')
no_fix = Database['fix_name'].isna()
Database['County'] = Database['County'].where(no_fix,Database['fix_name'])
Database = Database.drop(columns='fix_name')



#  Count lynchings

db_counties = Database.groupby(["State", "County"]).size()
db_counties = db_counties.reset_index()



#  Check county names

sm_county = Statemap.groupby(["STUSPS", "NAME"]).size()
sm_county = sm_county.reset_index()

Join = sm_county.merge(db_counties, 
                       left_on = ["STUSPS", "NAME"],
                       right_on = ["State", "County"],
                       how = "outer",
                       validate = "1:1",
                       indicator = True)

not_found = Join.query('_merge == "right_only"')
Join = Join.drop(columns = "_merge")
if len(not_found) > 0:
    print( 'Counties not found:', len(not_found) )
    not_found = not_found[['State','County']]
    print( not_found )
else: 
    print('all counties match')    
    
#This drops exactly one record for Campbell County Georgia which doesn't exist anymore

print(len(Join))

Join = Join.dropna(subset = "STUSPS")

print(len(Join))

#  Join onto the county map

#geo_zip = gpd.read_file("cb_2020_us_county_500k.zip")
geo_zip = Statemap.copy()
is_city = geo_zip["NAMELSAD"].str.contains(" city")
geo_zip = geo_zip[~is_city]
joined = geo_zip.merge(Join,
                    left_on=["STUSPS", "NAME"],
                    right_on=["STUSPS", "NAME"],
                      how ='outer',
                      validate='1:1',
                      indicator=True)

print(joined['_merge'].value_counts())
joined = joined.drop(columns="_merge")
joined.to_file("joined.gpkg", index=False)

geo_state = gpd.read_file("cb_2019_42_zcta510_500k.gpkg")
geo_state.to_file("joined.gpkg",index=False)

