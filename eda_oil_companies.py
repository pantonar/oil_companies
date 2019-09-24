#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pablo
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np

###############################################################################
#                                                                             #
#                   SET UP WORKING DIRECTORY                                  #       
#                                                                             #
###############################################################################
directory = r'/Users/pablo/Desktop/data_science_meetups/count_oil_companies'
os.chdir(directory)

###############################################################################
#                                                                             #
#                   LOAD DATA                                                 #       
#                                                                             #
###############################################################################
names = {'company_operational' : 'a',
         'company_financial'   : 'b',
         'country_economy'     : 'c',
         'country_industry'    : 'd',
         'oil_gas_price'       : 'e'}

# load all datasets
for name in names:
    names[name] = pd.read_csv(names[name]+'.csv')
    if name == list(names.keys())[0]:
        data = names[name]
    elif name == list(names.keys())[1]:
        data = pd.merge(data, names[name], how ='outer', on = ['company','country_iso','year'])
    elif name in list(names.keys())[2:4]:
        data = pd.merge(data, names[name], how ='left', on = ['country_iso','year'])
    else:
        data = pd.merge(data, names[name], how ='left', on = 'year')
    
# set as panel data
        
data.set_index(['company','year'],inplace = True)
data.reset_index(inplace = True)
########################3 add features
#world reserves
world_reserves = data.groupby(['year']).agg(sum)['oil_&_gas_reserves_boe_y']
a=dict(zip(world_reserves.index,world_reserves))
data['world_reserves'] = data['year'].map(a)
# others reserves
data['other_reserves'] = data['world_reserves'] - data['oil_&_gas_reserves_boe_y'] 
data['log_other_reserves'] = data['other_reserves'].apply(lambda x: np.log(x))
# year
data['year_only'] = data['year'].apply(lambda x: int(x[0:4]))
# CAPEX
global_capex = data.groupby(['year']).agg(sum)['capital_expenditures_usd_million']
data = data.merge(global_capex, on = 'year')

data = data.rename(columns = {'capital_expenditures_usd_million_y':'GlobalCAPEXYear'})
data['GlobalCAPEXOther'] = data['GlobalCAPEXYear'] - data['capital_expenditures_usd_million_x']
data['log_capex'] = data['capital_expenditures_usd_million'].apply(lambda x: np.log(x))
# Liabilities over assets
data['LiabilitiesOverAssets'] = data['total_liabilities_usd_million'] / data['total_assets_usd_million']
 
###############################################################################
#                                                                             #
#                   EXPLORE DATA                                              #       
#                                                                             #
###############################################################################
colnames = list(data.columns)

###############################################################################
#                                                                             #
#                   DRAW GRAPHS                                               #       
#                                                                             #
###############################################################################
fig, ax = plt.subplots(1, figsize=(10,6))
sns.regplot('year_only','other_reserves',data = data, color="g", ax = ax,
            label = 'reserves',
            marker = '.')
plt.ylabel('Reserves of rest of the world')
plt.xlabel('year')
ax2 = plt.twinx()
sns.regplot('year_only','capital_expenditures_usd_million',data = data, color="r",
            ax = ax2, label = 'Company CAPEX',
            marker = '.')
ax2.set_ylabel('CAPEX')
plt.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)

plt.savefig('cuisi.png')
        

fig, ax = plt.subplots(1, figsize=(10,6))
ax.scatter(x = data['oil_&_gas_reserves_boe_y'],
           y = data['total_liabilities_usd_million']
           )













        
    
        
        

            
            
            
            
            
            
            