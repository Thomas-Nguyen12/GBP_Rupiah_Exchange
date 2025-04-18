# Forecasting British GBP to Indonesian Rupiah Exchange Rates

## Project Description 
Many international students constantly check exchange rates when withdrawing their allowances. This requires persistant back-and-forth checking between local websites and the memory
to do so. As such, international students are constantly distracted from their studies and are unaware of key dates to check. 
This project aims to help international students predict key dates between the British pound (GBP) and the Indonesian Rupiah (IDR). As such, they can focus on their studies and
understand how exchange rates have changed over time. 

## How to use:
1. <b>Data Extraction:</b> Data was extracted using the <b>BeautifulSoup</b> package run within <b>currency_data_extraction.py</b> which can be executed using:
```python3 currency_data_extraction.py```

3. <b>Forecasting:</b> The forecaster can be found within: <b>forecaster.py</b> and uses <b>scalecast</b> as a TSA forecasting library and <b>Grids.py</b> to tune the models used in the forecasting which can be executed using:
```python3 forecaster.py```

5. <b>Dashboard:</b> This dashboard uses Streamlit to host the data, found within: <b>currency_streamlit.py</b> which can be run via:
```streamlit run currency_streamlit.py```

## Packages
This project utilises python 3.11.3 and its packages are found within <b>requirements.txt</b>: 

- beautifulsoup4==4.12.3
- bokeh==3.5.0
- joblib==1.4.2
- matplotlib==3.9.1.post1
- numpy==1.26.4
- pandas==2.2.2
- prophet==1.1.5
- Requests==2.32.3
- SCALECAST==0.19.8
- scipy==1.14.0
- seaborn==0.13.2
- streamlit==1.37.0

