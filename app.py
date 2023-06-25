import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

df_time_gender = pd.read_csv('./data/TimeGender.csv')
df_case = pd.read_csv('./data/Case.csv')
df_case = df_case[(df_case['latitude'] != '-') & (df_case['longitude'] != '-')]
df_case['latitude'] = df_case['latitude'].astype('float')
df_case['longitude'] = df_case['longitude'].astype('float')

st.title('COVID-19 Statistics')

st.title('Confirmed and deceased cases per selected sex')

selected_sex = st.selectbox('Select sex', df_time_gender['sex'].unique())
filtered_df = df_time_gender[df_time_gender['sex'] == selected_sex]

st.subheader(f'Confirmed cases for {selected_sex}')
st.line_chart(filtered_df, x='date', y='confirmed')

st.subheader(f'Deceased cases for {selected_sex}')
st.bar_chart(filtered_df, x='date', y='deceased')

st.title('COVID-19 Cases on Map')

selected_province = st.selectbox('Select province', df_case['province'].unique())
filtered_df = df_case[df_case['province'] == selected_province]

m = folium.Map(location=[filtered_df['latitude'].mean(), filtered_df['longitude'].mean()], zoom_start=8)

for index, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['city']} - {row['infection_case']}\nConfirmed cases: {row['confirmed']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

st.subheader(f'COVID-19 Cases in {selected_province}')
folium_static(m)
