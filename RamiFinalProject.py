# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:23:03 2022

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
fig2.suptitle('Lynchings by state by year')
Byyear.plot.area(ax = ax2, fontsize = 7, stacked = True)


