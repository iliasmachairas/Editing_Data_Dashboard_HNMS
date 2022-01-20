# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 01:07:49 2022

@author: ilias
"""

import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout = "wide")

st.markdown("""# Weather data - EMY - Greece""")

col2, space2, col3 = st.columns((10,1,10))

with col2:
    # Read data
    upload_data = st.file_uploader('Select the file', type=['csv'])
    if upload_data is not None:
        data = pd.read_csv(upload_data, skipinitialspace=True, delimiter=';', thousands=r'.', decimal=',')
        
        st.write(data.shape)
        cols = data.columns
        for i in cols[1:]:
            data[i] = pd.to_numeric(data[i])
        
        
        # Date manipulation
        data['OBSERVATIONYEAR'] = pd.to_numeric(data['OBSERVATIONYEAR'], downcast='integer')
        data['OBSERVATIONMONTH'] = pd.to_numeric(data['OBSERVATIONMONTH'], downcast='integer')
        data['OBSERVATIONDAY'] = pd.to_numeric(data['OBSERVATIONDAY'], downcast='integer')
        data['OBSERVATIONHOUR'] = pd.to_numeric(data['OBSERVATIONDAY'], downcast='integer')
        data.rename(columns={'OBSERVATIONYEAR':'year', 'OBSERVATIONMONTH':'month', 'OBSERVATIONDAY':'day'}, inplace=True)
        data['year'] = data['year'].astype('int8')
        st.text(data.columns)
        
        # Bull values for each column
        null_stats_Series =  (data.isnull().sum() / data.shape[0] * 100)
        st.write(null_stats_Series)
        
        data['date'] = data['year'].map(str) + '-' + data['month'].map(str) + '-' + data['day'].map(str)
        data['date'] = pd.to_datetime(data['date'])
        st.text(data.dtypes)
        
        #null_stats_Series =  (data.isnull().sum() / data.shape[0] * 100)
        #null_stats_Series.plot.barh()
        
        #st.text(data.date)
        # data['date'] = pd.to_datetime(data['date'])
        # st.text(type(data.date))
        # st.write('Ryn')
        # data.drop(columns=['year', 'month', 'day'], axis=1, inplace=True)
        # data.set_index('date', inplace=True)
        # st.text(data.dtypes)
        
with col3:
    st.text('Col3')
    
    #     null_stats_Series =  (data.isnull().sum() / data.shape[0] * 100)
    #     null_stats_Series.plot.barh()
    
    #st.text('Hello world')
    #st.text(data.shape)