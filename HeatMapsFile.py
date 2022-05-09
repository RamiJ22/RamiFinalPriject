# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:34:32 2022
​
@author: Rami
"""
import pandas as pd
import geopandas as gpd
​import matplotlib.pyplot as plt
​
import csv
​
import numpy as np
​
import seaborn as sns
​
import requests
#Filters the states down the ones with lynchings
Statemap = gpd.read_file("cb_2020_us_county_500k.zip")
#States in this list - AL - TN
States = ["01","05","12","13","21","22","28","37","45","47"] 
Statemap = Statemap[ Statemap['STATEFP'].isin(States)]
​
#Writes geopackage file
Statemap.to_file("Statemap.gpkg", layer = "counties", index=False)
fig, ax1 = plt.subplots(dpi=300)
​
fig.suptitle("States")
Statemap.plot(ax=ax1)
ax1.axis("off")
fig.savefig('Statemap.png')
​
#%%
​
#  Read a file of spelling corrections
​
fixup = pd.read_csv('fixup.csv')
fixup = fixup.dropna(subset='fix_name')
​
Database = pd.read_excel("HAL.XLS", dtype=str)
Database["County"] = Database["County"].str.strip()
​
#  Remove entries with unknown counties
​
Database = Database.query("County != 'Indeterminant'")
Database = Database.query("County != 'Undetermined'")
​
#  Correct misspellings
​
Database = Database.merge(fixup,on=['State','County'],how='left')
no_fix = Database['fix_name'].isna()
Database['County'] = Database['County'].where(no_fix,Database['fix_name'])
Database = Database.drop(columns='fix_name')
​
#  Count lynchings
​
db_counties = Database.groupby(["State", "County"]).size()
db_counties = db_counties.reset_index()
​
#%%
​
#  Check county names
​
sm_county = Statemap.groupby(["STUSPS", "NAME"]).size()
sm_county = sm_county.reset_index()
​
Join = sm_county.merge(db_counties, 
                       left_on = ["STUSPS", "NAME"],
                       right_on = ["State", "County"],
                       how = "outer",
                       validate = "1:1",
                       indicator = True)
​
not_found = Join.query('_merge == "right_only"')
​
if len(not_found) > 0:
    print( 'Counties not found:', len(not_found) )
    not_found = not_found[['State','County']]
    print( not_found )
else: 
    print('all counties match')    
​
#%%
​
#  Join onto the county map