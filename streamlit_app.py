import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import pydeck as pdk
import shapefile as shp
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from pprint import pprint
import json

st.set_page_config(page_title='HAITI -  Cereal Price',
                   layout='wide', page_icon=':cereal:')


t1, t2 = st.columns((0.01, 1.08))
# t1.image('haiti-flag-square.jpg', width=120)
t2.title("Evolution of Haiti Population from 1982 to 2015")
t2.markdown(" **tel:** 509 36055983 **| email:** mailto:vitalralph@hotmail.com")
t2.markdown(" **Wikipedia** ")


@st.cache_data
def get_original():
    depart_path  = Path(__file__).parent/'data/depart_coord_pop.csv'
    depart_df = pd.read_csv(depart_path)
    return depart_df



population_df = get_original()

all_department = ['all'] + list(population_df['Department'].unique())
disable = False
with st.sidebar:
    st.write('Parameters: ')
    d_option = st.selectbox(
        "Choose a department",
        tuple(all_department),
    )
    if d_option == 'all':
        disable = True
    else:
        disable = False
      
    label =  st.selectbox(
    "Choose a year",
    list(population_df['year'].unique()),
)

population_df = get_original()
if d_option == 'all':
    filter_pop = population_df[population_df['year'] == label]
else :
    filter_pop = population_df[(population_df['year'] == label) &
                               (population_df['Department']==d_option)]

print(filter_pop.head())

m = folium.Map(location=[18.53, -72.33], zoom_start=7.45,width=1000,height=600, )
group_1 = folium.FeatureGroup("HAiti  Population").add_to(m)
for ele in filter_pop.to_dict(orient='records'):
    folium.Marker(
     location=[ele['Latitude (EPSG:4326)'], ele['Longitude (EPSG:4326)']],
     popup="<b>Departemen:</b>{} <br> <b>Population:</b>  {} <br>   <b>Year:</> {}".format(ele['Department'],int(ele['Value']), ele['year'][-4:]),
  ).add_to(group_1)
#folium.GeoJson(road_json, name="Haitian roads").add_to(m)
#folium.GeoJson(airp_json, name="Haitian airports").add_to(m)
folium.LayerControl().add_to(m)
st_folium(m, width=1000, height=500)


