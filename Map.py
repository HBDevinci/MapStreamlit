import folium 
import streamlit as st 
from streamlit_folium import st_folium 
import csv 
import pandas as pd
import Treatment
import numpy as np
from folium.plugins import MarkerCluster



def read_data(dataset):
    # Convert the 'latitude', 'longitude', and 'ScientificName' columns to a list of dictionaries
    data = dataset[['latitude', 'longitude', 'ScientificName']].astype({'latitude': float, 'longitude': float, 'ScientificName': str}).to_dict(orient='records')
    return data


dates_selected_int = [int(valeur) for valeur in Treatment.dates if pd.notna(valeur)]
dates_selected_str = [str(valeur) for valeur in dates_selected_int]


#data_1842_1900 = read_data(Treatment.subset_1842_1900)
#data_1901_1950 = read_data(Treatment.subset_1901_1950)
#data_1951_2000 = read_data(Treatment.subset_1951_2000)
#data_2001_2016 = read_data(Treatment.subset_2001_2016)

LOCATION_CENTER = (26.513076975660177, -80.78559180798361)


st.header("Coral Reef", divider = "rainbow")


start_date, end_date = st.select_slider(
    'Select a period',
    options=dates_selected_str,
    value=('1842', '2016'))
st.write('You selected period between', start_date, '-', end_date)

start_date_float = float(start_date)
end_date_float = float(end_date)

m = folium.Map(location=LOCATION_CENTER, zoom_start=5)

marker_cluster = MarkerCluster().add_to(m)


if (start_date_float and end_date_float) in dates_selected_int and start_date_float < end_date_float:
    data_to_display = read_data(Treatment.reefs_sorted.loc[Treatment.reefs_sorted['ObservationYear'].between(start_date_float, end_date_float)])
    for coral in data_to_display:
    # Créer un marqueur pour chaque corail avec une fenêtre contextuelle contenant son nom scientifique
        folium.Marker(
            location=[coral['latitude'], coral['longitude']],
            popup=folium.Popup(f"{coral['ScientificName']}", parse_html=True)
        ).add_to(marker_cluster)
else:
    st.write("Please select a valid period.")
    data_to_display = None

#if data_to_display is not None:
#    st.map(data_to_display)

# Afficher la carte dans Streamlit
st_data = folium.Figure(width=750, height=500)
st_data.add_child(m)
st_folium(st_data, width=750, height=500)