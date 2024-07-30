import streamlit as st 
import numpy as np 
import scipy.stats as stats 
import matplotlib.pyplot as plt 
import seaborn as sns 
from scalecast.Forecaster import Forecaster 
import itertools
from bokeh.palettes import inferno
from bokeh.plotting import figure
import pandas as pd 
from currency_data_extraction import *
import joblib 
import pickle

from scalecast.Forecaster import Forecaster  
import warnings
warnings.filterwarnings("ignore")


# Loading the forecast image line boundary data

date_line_boundary = joblib.load("date_line_boundary.joblib")

## Importing the dataset


df['date'] = df.index

years_collected = [int(i) for i in years.keys()]

## Loading the saved forecaster model 
# THis can be pretrained? (model.save)


## setting the page configuration 
st.set_page_config(page_title="IDR/GBP currency exchange data", layout="wide")


# Header
with st.container(): 
    st.subheader("This website shows currency exchange data from 2015 onwards")
    

with st.container(): 
    st.write("--------") 
    
    left_column, right_column = st.columns(2) 
    
    with left_column: 
        st.header("Goals")
    
    
    with right_column: 
        st.header("")
        

## historical data 
# I should show options for months, years, days, 
# Include sliders (to specify time periods) and drop-down menus (to specify days, months, and years)



with st.container(): 
    # The left column shows options
    # The right column vizualises data
    left_column, right_column = st.columns(2) 


    with left_column: 
        
        ## The time period depends on the time category
        
        
        ## Make sure to scan the current years
        # I can create a slider for days, months, years? 
        
        # I need to make sure that the year_slider updates itself for the current year
        
        # The values are in the 'years' dictionary
        
        
        year_slider = st.slider(
            
            f"Select years, {min_year} :: {max_year}",
            # I can use this to specify the x axis
            # to do this, I can create a subset
            min_year, max_year, (2017, 2020))
        
        # Creating a subset 
        
        # I need to specify rows but all columns
        
        month_slider = st.slider(
            'Select months',
            
            1, 12, (4, 6)
            
        )
        
        if month_slider == 1 or 3 or 5 or 7 or 8 or 10 or 12: 
            day_slider = st.slider(
                'Select Days',
                1, 31, (10, 12)
            )
        else: 
            day_slider = st.slider(
                'Select Days',
                1, 30, (10, 12)
            )
            
        
        # remember that not all months have the same number of days
                
        
        
        
        # the year slider is a tuple
        # I will need to find the dataframe rows between the certain values
        
        time_period1 = pd.to_datetime(f"{year_slider[0]}/{month_slider[0]}/{day_slider[0]}")
        time_period2 = pd.to_datetime(f"{year_slider[1]}/{month_slider[1]}/{day_slider[1]}")

        
        ## Indexing the dataframe 
        
        specific_df = df.loc[time_period1:time_period2]        
    # Vizualising data
    with right_column: 
        current_tab, forecast_tab = st.tabs(['current', 'forecast'])
        ## Within this column, I can create two tabs for the current data, and the predictions
        
        
        
        # I could use interactive plots 
        # I should be able to modify the graph based on the 
        # select boxes
        
        ## I can vary the data by... 
        # creating new dataframes? 
        # (specifying row numbers and stuff)
        
        
        
        
        ## Graph (interactive)
        with current_tab:
            st.header('Historical Data')
            st.write(f"Last updated: {max(df.index)}")
            st.line_chart(data=specific_df, x="date", 
                        y="rupiahs_in_a_pound")
            
        with forecast_tab: 
            ## Here, I insert the forecast data 
            # I can update this every week/month? 
            
            # I could just present a graph here (interactive?)
            st.header('forecast data')
            
            
            st.image('forecast.png')
            
            # How often should I update this model? 
            
            ## Importing the pre-loaded forecaster 
            
            # Loading the forecaster 
            st.write(f"This forecaster was last updated at: {date_line_boundary}")
            
            
            
            
print ('---------')
print ("index") 

