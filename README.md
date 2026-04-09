# Forecasting British GBP to Indonesian Rupiah Exchange Rates


## March 2026 update
<b>Please note</b> that the webscraper (currency_data_extraction.py) that this project uses has broken due to website changes, with few viable alternatives. Consequently, some of the files (file tree listed below) are broken. However, data up until 2024 has been saved and is viewable on the streamlit dashboard. I will be searching for an alternative and will fixed in due course.

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

## Project Structure 

```
.
├── currency_streamlit.py   # Main dashboard
├── data
│   ├── all_data.csv  # scraped exchange data up until April 2024
│   ├── date_line_boundary.joblib  # boundary line indicating where the forecast begins
│   ├── date_line_boundary.pkl
│   ├── forecaster.joblib   
│   ├── forecaster.pkl
│   └── IDR_forecast.xlsx   # forecast predictions saved in excel format
├── forecast.png   # Image of the currency exchange forecast
├── models
│   └── lstm_forecaster.h5
├── notebooks
│   └── english_indonesian_exchange.ipynb
├── README.md
├── requirements.txt
└── scripts
    ├── currency_data_extraction.py
    ├── currency_data_extraction2.py   # attempt at reconfiguring the web scraper to account for website changes
    ├── diagnose_page.py   # script to detect changes in the website
    ├── diagnose_page2.py  # additional script to detect changes in the website
    ├── forecaster.py   # script to create a GBP/IDR forecaster model 
    └── Grids.py   # additional algorithms to incorporate into the forecaster

```


## Packages
This project utilises python 3.11.3 and its packages are found within <b>requirements.txt</b>: 
```
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
```
