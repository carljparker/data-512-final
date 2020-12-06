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
# Prior to <span style="color:red">May 25, 2020</span>, COVID-19 deaths in the United States were falling precipitously. On May 25th, that descent slowed dramatically, and then, around the beginning of July, reversed itself, starting a second wave of COVID-19 deaths in the United States. The number of deaths in this second wave, 125K, now exceeds that of the first wave, 100K.
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
import pandas as pd

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
trump_rallies.tail()

# %%
trump_rallies.shape

# %%
target_location = trump_rallies.loc[ 0, "City" ] + ", " + trump_rallies.loc[ 0, "State" ]
target_location

# %%
g = geocoder.bing( target_location, key=os.environ[ 'BING_API_KEY' ] )
g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] 

# %%
geocoder.bing( 'The Villages' + ", " + 'FL', key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ]

# %%
geocoder.bing( 'The Villages' + ", " + 'FL', key=os.environ[ 'BING_API_KEY' ] ).json[ 'raw' ][ 'address' ]


# %%
def gcode( row ):
    g = geocoder.bing( row[ 'City' ] + ", " + row[ 'State' ], key=os.environ[ 'BING_API_KEY' ] )
    if 'adminDistrict2' in g.json[ 'raw' ][ 'address' ]:
        county = g.json[ 'raw' ][ 'address' ][ 'adminDistrict2' ] 
        return( county )
    else:
        return( 'Sumpter County' )



# %%
trump_rallies[ 'County' ] = trump_rallies.apply( gcode, axis = 1 )

# %%
trump_rallies.loc[ : , 'County' ].head()

# %%
trump_rallies.loc[ : , 'County' ].tail()

# %% [markdown]
# # Read time series data from Johns-Hopkins COVID-19 repository #

# %%
covid_19_time_series_by_county = pd.read_csv('data/time_series_covid19_deaths_US.csv', 
        sep=',', 
        comment='#',
        skipinitialspace=True,
        header=0,
        na_values='?')

# %%
covid_19_time_series_by_county.shape

# %%
covid_19_time_series_by_county.head()

# %%
covid_19_time_series_by_county.tail()

# %% [markdown]
# Most of the columns are the COVID-19 deaths for a given date. Show the non-date columns.

# %%
covid_19_time_series_by_county.columns.array[ 0:12 ]

# %% [markdown]
# The `Admin2` column contains the county. There are many duplicates in that column; we can't merge on it.

# %%
len( covid_19_time_series_by_county.loc[ :, 'Admin2' ] ) 

# %%
len( covid_19_time_series_by_county.loc[ :, 'Admin2' ].unique() )

# %% [markdown]
# The `Combined_Key` column provides a _primary key_ that uniquely identifies the row.

# %%
covid_19_time_series_by_county.loc[ :, 'Combined_Key' ]

# %% [markdown]
# Remove unneeded columns.

# %%
covid_19_time_series_by_county.drop( [ 'UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region' ] , axis = 1, inplace = True )

# %%
covid_19_time_series_by_county.head()

# %% [markdown]
# # Synthesize a key for the Trump rallies dataframe to use for merging #

# %% [markdown]
# Read in a dataset that maps from state names to state abbreviations.

# %%
state_abbr = pd.read_csv('data/state-abbr.csv', 
        sep=',', 
        comment='#',
        skipinitialspace=True,
        header=0,
        na_values='?')

# %%
state_abbr.head()

# %%
state_abbr.tail()

# %% [markdown]
# Create a dictionary from the two columns of our state/abbr dataframe.

# %%
map_abbr_state = dict( zip( state_abbr.Abbr.str.strip(), state_abbr.State.str.strip() ) )

# %%
map_abbr_state.keys()

# %%
map_abbr_state[ 'VA' ]


# %%
def create_combined_key_for_trump( row ):
    combined = row[ 'County' ][ 0:-6 ].rstrip() + ", " + map_abbr_state[ row[ 'State' ] ] + ", " + 'US'
    return combined

trump_rallies[ 'Combined_Key' ] = trump_rallies.apply( create_combined_key_for_trump, axis = 1 )

# %%
trump_rallies[ 'Combined_Key' ].head()

# %%
trump_rallies.head()

# %% [markdown]
# # Merge Trump rallies data with COVID-19 data #

# %%
trump_rallies = trump_rallies.merge( covid_19_time_series_by_county, how = "left", on = "Combined_Key")

# %%
trump_rallies.columns

# %%
trump_rallies.shape

# %%
trump_rallies.head()

# %% [markdown]
# # Derive a table that has only the COVID-19 deaths by rally location #

# %% [markdown]
# Drop columns that are unecessary for this table

# %%
covid_19_deaths_by_rally = trump_rallies.drop( ["Date", "City", "State", "County", "Lat", "Long_", "Population" ], axis = 1 )
covid_19_deaths_by_rally.head()

# %% [markdown]
# Swap the rows and columns

# %%
covid_19_deaths_by_rally = covid_19_deaths_by_rally.transpose()
covid_19_deaths_by_rally.head()

# %% [markdown]
# Use the first row as the column labels

# %%
covid_19_deaths_by_rally.columns = covid_19_deaths_by_rally.iloc[0]
covid_19_deaths_by_rally.drop(covid_19_deaths_by_rally.index[0], inplace = True )
covid_19_deaths_by_rally.head()

# %% [markdown]
# Fix up name of first column

# %%
covid_19_deaths_by_rally.columns.name = ""
covid_19_deaths_by_rally

# %% [markdown]
# # Remove the COVID-19 deaths from the Trump rallies table #

# %%
trump_rallies.drop( trump_rallies.iloc[:, 8:], axis = 1, inplace = True )
trump_rallies.head()

# %% [markdown]
# ### --- END --- ###
