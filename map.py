import dash
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import folium
import urllib, json

#---------------------------------------
indicators = pd.read_csv('Indicators.csv')
indicators.tail(5)
# new_data = pd.read_csv('WDIData.csv')
new_busi = indicators[indicators['IndicatorCode'].str.match(r'(^IC.*)')]

# Check for null values
new_busi.isnull().sum()

xq = new_busi.query('IndicatorCode=="IC.BUS.EASE.XQ"')



#
finance = indicators[indicators['IndicatorCode'].str.match(r'(^DT.*)')]
# finance.IndicatorName.unique()

# External debt stocks, total (DOD, current US$)
ex_debt_stocks= finance.query('IndicatorCode=="DT.DOD.DECT.CD"')
# Get the top 10 countries in terms of external debt stocks
top_10 = ex_debt_stocks.groupby('CountryName',as_index=False)[['Value']].mean().sort_values(by='Value',ascending=True).iloc[:10]
# Rank all the countries in terms of external debt stocks
debt_rank = ex_debt_stocks.groupby(['CountryCode','CountryName'],as_index=False)['Value'].mean()


# Choropleth map
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
json_url = urllib.request.urlopen(url)
geo_data = json.loads(json_url.read())

world_map = folium.Map(location=[100, 0], zoom_start=2)

folium.Choropleth(
    geo_data=geo_data,
    data=debt_rank,
    columns=['CountryCode','Value'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.6,
    line_opacity=1,
    legend_name="Total external debt stocks"
).add_to(world_map)

