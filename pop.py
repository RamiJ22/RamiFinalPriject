# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 06:43:27 2022

@author: Rami
"""

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

import csv

import numpy as np

import seaborn as sns

import requests 

fips = "01"
po = "AL"

api = 'https://api.census.gov/data/2018/acs/acs5'  

for_clause = "county:*"

#for - indicates what kind of geographic unit should be returned & select subsets of the possible records 

#* wildcard indicating that data for all eligible counties 

 
#Puts in whatever fips code is set on line 21
in_clause = f'state:{fips}' 

#in - limit selected geo units  

#counties in state 36(NY) 

 

key_value = '1a285d24c0d40e958811435eaaf09466ac365484' 

 
#People who identify as Black alone
payload = { 'get':"NAME,B02001_003E", 'for':for_clause, 'in':in_clause, 'key':key_value }

response = requests.get(api, payload) 

#will build HTTPS query string, send to API endpoint, collect response 

 

if response.status_code == 200:  

    print('\nThe request succeeded') 

else: 

    print('\n',response.status_code,'\n',response.text) 

    assert False 

#this will cause script to stop immediately if statement is reached 

 

row_list = response.json() 

#parse JSON returned by Census server and return rows  

 

colnames = row_list[0] 

#check this 

 

datarows = row_list[1:] 

 

pop = pd.DataFrame(columns=colnames, data=datarows)
pop["GEOID"] = pop["state"] + pop["county"]
#Renames roqs

#Changes columns
#Use state postal code at the send of the file, helping you label and know which state you're looking at 
pop.to_csv(f'pop_{po}.csv')                             