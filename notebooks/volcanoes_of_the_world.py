#import libraries
import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from copy import deepcopy

#import data
with open('./data/raw/countries.geojson') as response:
    geojson = json.load(response)

#create cache with raw_df inside
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

df_raw = load_data(path='./data/raw/volcano_ds_pop.csv')
df = deepcopy(df_raw)

df['Country'] = df['Country'].replace({'United States':'United States of America',
                                            'Tanzania':'United Republic of Tanzania',
                                            'Martinique':'Martinique',
                                            'Sao Tome & Principe':'Sao Tome and Principe',
                                            'Guadeloupe':'Guadeloupe',
                                            'Wallis & Futuna':'Wallis and Futuna'})

df_vol_dens = df.groupby('Country').agg('count')
df_vol_dens['Volcanoy-est'] = df_vol_dens['Volcano Name']


st.title('Volcanos of the World 🌋')
st.header('Learn about the world\'s volcanos.')




maps = ['Which countries have the most volcanos?', 'Where are the world\'s volcanos?']
map_choice = st.radio('Choose Which Map to See:', maps)

#plotly fig which shows the which countries have the most volcanos
fig_most = px.choropleth_mapbox(
    df_vol_dens, 
    geojson=geojson, 
    color='Volcanoy-est', 
    locations=df_vol_dens.index, 
    featureidkey="properties.ADMIN",
    mapbox_style="carto-darkmatter", 
    zoom=0,
    color_continuous_scale='reds',
    width=950,
    height=450,
    opacity=0.6)

#plotly fig which shows the locations of volcanos around the world.
fig_locations = px.scatter_mapbox(
    df, 
    lat='Latitude',
    lon='Longitude',
    text='Volcano Name',
    mapbox_style="carto-darkmatter",
    size_max=1, 
    zoom=0,
    color_discrete_sequence=["red"],
    width=950,
    height=450,
    opacity=0.6)

if map_choice == 'Which countries have the most volcanos?':
    st.plotly_chart(fig_most, use_container_width=True)
    st.text_area('The world is so volcanoy!', 'Here you can see which countries have the most volcanos. Also, countries which show in black have no volcanos.')
else:
    st.plotly_chart(fig_locations, use_container_width=True)
    st.text_area('The world is so volcanoy!', 'Here you can see where all of the worlds volcanos are located. I am glad I live in Germany')

