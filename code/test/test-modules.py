import os
import datetime
import re
import geocoder
import numpy as np
import pandas as pd
import descartes
import geopandas as gpd
# from matplotlib import pyplot as plt

import constants

g = geocoder.bing( 'Kenosha,s WI', key=os.environ[ 'BING_API_KEY' ] )

print( g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )

trump_rallies = pd.read_csv('data/trump-rallies.csv', 
        sep=',', 
        comment='#',
        skipinitialspace=True,
        header=0,
        na_values='?')

# %%
trump_rallies.columns

# %%
trump_rallies.head()

# %%
trump_rallies.tail()

# %%
trump_rallies.shape


# --- END --- #

