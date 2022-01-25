# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 01:07:49 2022

@author: ilias
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

st.set_page_config(layout = "wide")

st.markdown("""# Weather data - EMY - Greece""")

col2, space2, col3 = st.columns((10,1,10))

with col2:
    # Read data
    upload_data = st.file_uploader('Select the file', type=['csv'])
    if upload_data is not None:
        data = pd.read_csv(upload_data, skipinitialspace=True, delimiter=';', thousands=r'.', decimal=',')
        
        #st.write(data.shape)
        cols = data.columns
        for i in cols[1:]:
            data[i] = pd.to_numeric(data[i])
        
        # Date manipulation
        data['OBSERVATIONYEAR'] = pd.to_numeric(data['OBSERVATIONYEAR'], downcast='integer')
        data['OBSERVATIONMONTH'] = pd.to_numeric(data['OBSERVATIONMONTH'], downcast='integer')
        data['OBSERVATIONDAY'] = pd.to_numeric(data['OBSERVATIONDAY'], downcast='integer')
        data['OBSERVATIONHOUR'] = pd.to_numeric(data['OBSERVATIONHOUR'], downcast='integer')
        
        data.rename(columns={'OBSERVATIONYEAR':'year', 'OBSERVATIONMONTH':'month', 'OBSERVATIONDAY':'day', \
                             'OBSERVATIONHOUR':'hour'}, inplace=True)
        data['year'] = data['year'].astype('int8')
        data['hour'] = data['hour'].astype('str')
        data['hour'].replace('0', '00', inplace=True)
        data['hour'].replace('3', '03', inplace=True)
        data['hour'].replace('6', '06', inplace=True)
        data['hour'].replace('9', '09', inplace=True)
        # Null values for each column
        null_stats_Series =  (data.isnull().sum() / data.shape[0] * 100)
        
        data['date'] = data['year'].map(str) + '-' + data['month'].map(str) + '-' + data['day'].map(str)+' ' + data['hour']
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.drop(columns=['year', 'month', 'day', 'hour'], axis=1, inplace=True)
        #st.text(data.dtypes)
        data_daily = data.resample('D').mean()
        min_date = data_daily.index.min().date()
        max_date = data_daily.index.max().date()
        mean_date = data_daily.index.mean().date()
        
        # Select Dates
        # Check checkbox first - Select part of data
        date_range_yes = st.checkbox('Select a specific date range', False)
        
        if date_range_yes == True:
            start_date = st.date_input('Select start date', \
                                       value=mean_date, min_value=min_date, max_value = max_date, key=1)
            
            end_date = st.date_input('Select end date', \
                                     value=mean_date + datetime.timedelta(days=1), min_value=min_date, \
                                     max_value = max_date, key=2)
            if end_date<start_date:
                st.error('end_date should be larger than start_date')
                
        #st.date_input('Select the date after which latest update of the app took place', value=mean_date, min_value=min_date, max_value = max_date)
        
        
        # Select parameter
        selected_cat = st.selectbox(label='Select parameter', options=data.columns)
        
        st.markdown(f'<h1 style="color:#19C8CA;font-size:24px;">{"Null values"}</h1>', unsafe_allow_html=True)
        fig = px.bar(null_stats_Series, y=null_stats_Series.index, x=null_stats_Series.values, orientation='h')
        fig.update_layout(xaxis=dict(title='Null values Percentage (%)',titlefont_size=16, tickfont_size=14), \
                     yaxis=dict(title='Parameter',titlefont_size=16, tickfont_size=14))
        st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.subheader("Time Series of selected variable: "+str(selected_cat))
            time_ser_fig = go.Scatter(x=data_daily.index, y=data_daily[selected_cat])
            fig = go.Figure(time_ser_fig)
            fig.update_layout(xaxis=dict(title='Time',titlefont_size=16, tickfont_size=14), \
                         yaxis=dict(title='Parameter value',titlefont_size=16, tickfont_size=14))
            st.plotly_chart(fig, use_container_width=True)
            
            
            
    #     null_stats_Series =  (data.isnull().sum() / data.shape[0] * 100)
    #     null_stats_Series.plot.barh()
    
    #st.text('Hello world')
    #st.text(data.shape)