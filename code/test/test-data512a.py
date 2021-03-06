# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Impact of Trump super-spreader rallies on COVID-19 deaths in United States #

# %% [markdown]
# This project investigates the possible effects of Trump campaign rallies on the spread of COVID-19 during the summer and early fall of 2020.

# %% [markdown]
# ## Background and Motivation ##

# %% [markdown]
# Prior to May 25, 2020, COVID-19 deaths in the United States were falling precipitously. On May 25th, that descent slowed dramatically, and then, around the beginning of July, reversed itself, starting a second wave of COVID-19 deaths in the United States. The number of deaths in this second wave, 125K, now exceeds that of the first wave, 100K.
#
# The date, May 25, 2020, is significant in that it is the date on which George Floyd died while in police custody in Minneapolis, MN. Subsequent to Floyd's death, protests occurred in over 2,000 cities in the United States. It has been suggested that the George Floyd Protests might have contributed to triggering the second wave of COVID-19. 
#
# This "hypothesis" is confounded, however, by summer political campaigning in the run up to the 2020 Elections. In particular, President Trump was notable for holding campaign rallies in which the president did not follow normative behavior to control COVID-19 infections and neither did many of the rally attendees--possibly following the president's lead. These became known as _super-spreader rallies_. Some news agencies have reported that COVID-19 infections spiked in the areas where these rallies had been recently held. However, I have not found a _systematic_ investigation of whether and to what extent the rallies were correlated with COVID-19 spread.

# %% [markdown]
# _**The yellow arrows in the two graphs below identify May 26, 2020, that is, the day after George Floyd died while in police custody.**_

# %% [markdown]
# ### COVID-19 deaths: Seven day moving average ###
#
# ![](viz/2020-10-23_original-screen-capture.png)

# %% [markdown]
# ### COVID-19 deaths: Cumulative ###
#
# ![](viz/2020-10-23_accumulated-deaths-anno.png)

# %% [markdown]
# ## Research Questions and Hypothesis ##

# %% [markdown]
# The key question is whether it is possible to identify increases in mortality from COVID-19 subsequent to President Trump's rallies and also relatively proximal to where the rallies were held. And further, to see if these increases are greater than we would expect when compared to changes in COVID-19 mortality during the same times periods in other locations.
#
# My hypothesis is that I _can_ identify increases in COVID-19 mortality associated with President Trump's rallies and that these increases are greater than we would expect based on contemporaneous COVID-19 mortality in other areas.

# %% [markdown]
# ## Data ##

# %% [markdown]
# For data that indicates the spread of COVID-19, I will use the _COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University_ hosted on GitHub at the following URL:
#
# >  <https://github.com/CSSEGISandData/COVID-19>
#
# For data on President Trump's campaign rallies, I will use the list maintained on Wikipedia at the following URL:
#
# >  <https://en.wikipedia.org/wiki/List_of_post-election_Donald_Trump_rallies#2020_campaign_rallies>

# %% [markdown]
# ## Methodology ##

# %% [markdown]
# The Johns-Hopkins data tracks COVID-19 deaths per county in the United States. Using geocoding, I can convert the City-State locations for President Trump's rallies into county locations. I should then be able to gather statistics for each of the counties which are also supported by the Johns-Hopkins data.
#
# I can also gather similar statistics for a set of counties where President Trump did _not_ hold rallies and use these as something analogous to _controls_.
#
# Specifically, the questions that I will investigate are, for each of the Trump rallies:
#
# - What was the change in the seven-day moving average for COVID-19 deaths in the 60 days _**before**_ the date of the Trump rally in that county--and in each of the control counties.
# - What was the change in the seven-day moving average for COVID-19 deaths in the 60 days _**after**_ the date of the Trump rally in that county--and in each of the control counties.
#
# - What was the total accumulated COVID-19 deaths in the 60 days _**before**_ the date of the Trump rally in that county--and in each of the control counties.
# - What was the total accumulated COVID-19 deaths in the 60 days _**after**_ the date of the Trump rally in that county--and in each of the control counties.
#
# And also:
#
# - Compare summary statistics (mean, median, std) for accumulated COVID-19 deaths in the Trump counties vs the control counties.
#
# To be clear, I will look at COVID-19 deaths in the control counties before and after the date of each Trump rally _even though no Trump rally occurred in that county_.

# %% [markdown]
# ## Unknowns ##

# %% [markdown]
# I have, so far, identified a couple unknowns that could affect the success of this investigation.
#
# One unknown is that Trump's rallies were not always held in an urban center. For example, some were held at airports. The president would fly in, speak at a rally at the airport, and then fly out. **In these cases, it is not certain where the attendees originated from; that is, we can't assume that they came from the nearest urban center.** 
#
# To take an example, on September 3, 2020, Trump spoke at a rally at Arnold Palmer Regional Airport outside Latrobe, PA. However, we can't necessarily infer from this that all the attendees were from Latrobe; they might have traveled in from out of area. More importantly, we don't know where the attendees traveled _to_ after the rally. 
#
# (Actually, this issue, that attendees might reside outside the area where the rally was held, applies to some degree even for rallies held inside city centers.)
#
# **Another unknown is that the locations of Trump's rallies are not uniformly distributed across the United States.** This could be for reasons such as campaign strategy. But in any case, regional differences between areas that hosted the rallies and those that didn't could introduce bias into the data.

# %%
import os
import geocoder
import numpy as np
import pandas as pd
import logging

#
# Configuration
#

#
# Log to a file at a level (threshold) of DEBUG.
#
# WARNING is the default level.
#
# If the file exists, we append to it. This is the default.
#
# To overwrite an existing log file, use:
#   
#   filemode='w'
#
# You can call logging.basicConfig() only once. Subsequent calls do not 
# have any effect.
#
logger = logging.getLogger(__name__)
logger.setLevel( logging.DEBUG )

#
# create console handler and set level to debug
#
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter( 
              fmt='[%(asctime)s] %(funcName)s( %(lineno)d ) %(levelname)s: %(message)s', 
              datefmt='%m-%d-%a %I:%M:%S %p' 
            )

#
# add formatter to ch
console_handler.setFormatter( formatter )

#
# add ch to logger
#
logger.addHandler( console_handler )

#
# End of logger configuration 
#

logger.info( "About to start program . . . [up to 35sec wait]" )


# %%
#
# Note that the BING_API_KEY variable needs to be set with your API key
# in the console window from which you launch this Jupyter notebook.
#
g = geocoder.bing( 'Kenosha,s WI', key=os.environ[ 'BING_API_KEY' ] )

print( g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )

# %%
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
trump_rallies.shape

# %%
trump_rallies.iloc[ 0, 1 ]

# %%
trump_rallies.loc[ 0, "State" ]

# %%
target_location = trump_rallies.loc[ 0, "City" ] + ", " + trump_rallies.loc[ 0, "State" ]
g = geocoder.bing( target_location, key=os.environ[ 'BING_API_KEY' ] )
target_location

# %%
g = geocoder.bing( trump_rallies.loc[ 0, "City" ] + ", " + trump_rallies.loc[ 0, "State" ], key=os.environ[ 'BING_API_KEY' ] )

# %%
geocoder.bing( trump_rallies.loc[ 0, "City" ] + ", " + trump_rallies.loc[ 0, "State" ], key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ][ 'address' ][ 'adminDistrict2' ]

# %%
print( g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )

# %%
trump_rallies.loc[ : , 'County' ] = geocoder.bing( trump_rallies.loc[ 0, "City" ] + ", " + trump_rallies.loc[ 0, "State" ], key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ][ 'address' ][ 'adminDistrict2' ]


# %%
def gcode( row ):
    logger.info( "Inside gcode...City: %s :: State: %s", row[ 'City' ], row[ 'State' ] )
    g = geocoder.bing( row[ 'City' ] + ", " + row[ 'State' ], key=os.environ[ 'BING_API_KEY' ] )
    if 'adminDistrict2' in g.json[ 'raw' ][ 'address' ]:
        county = g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] 
        logger.info( "City: %s :: State: %s :: Country: %s", row[ 'City' ], row[ 'State' ], county )
        return( county )
    else:
        logger.warning( "City: %s :: State: %s . . . No county found", row[ 'City' ], row[ 'State' ] )
        return( np.nan )


# %%
def gcode_np():
    return( geocoder.bing( 'Kenosha' + ", " + 'WI', key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] )


# %%
geocoder.bing( 'Kenosha' + ", " + 'WI', key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ][ 'address' ][ 'adminDistrict2' ]

# %%
gcode_np()

# %%
trump_rallies[ 'County' ] = trump_rallies.apply( gcode, axis = 1 )
trump_rallies.loc[ : , 'County' ].head()

# %% [markdown]
# ### --- END --- ###

# %%
