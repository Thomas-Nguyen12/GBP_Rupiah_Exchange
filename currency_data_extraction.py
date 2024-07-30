from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np 
import scipy.stats as stats 
import requests 

# Defining the web scraper 
# This will need to detect the latest year 





start_url = "https://www.exchange-rates.org/exchange-rate-history/idr-gbp"


# Turn into numbers 
html = requests.get(start_url)
soup = BeautifulSoup(html.text)
# I need to assign this to different years 
years = soup.select('ul.rates-by-year li')
year = [] 
for i in years: 
    print (i.text)
    year.append(int(i.text))
max_year = max(year) 
min_year = min(year)






def collect_data(year):
    start_url = f"https://www.exchange-rates.org/exchange-rate-history/idr-gbp-{year}" 

    # Turn into numbers 
    html = requests.get(start_url)
    soup = BeautifulSoup(html.text)
    # I need to assign this to different years 
   

    values_html = soup.select("table.history-rates-data tbody tr td")
    row_values_html = soup.select('table.history-rates-data tbody tr td')
    column_1 = soup.select("table thead tr th.ltr-bidi-fix")

    #############################################
    columns = [i.text for i in column_1]
    values = [i.text for i in values_html]


    ## I will need to parse through this...
    row_values = [i.get_text(separator=" ", strip=True) for i in row_values_html]


    ## collecting the table for historical data
    ## Making the dataframe 

    ## I need to use the .get_text(seperator=" ", strip=True)

    df = pd.DataFrame(row_values)

    ## Odd numbers shows the exchange rate 
    ## Even numbers show the date 


    exchange = [] 
    date = [] 

    for i in df.index: 
        
        if i % 2 == 0: 

            date.append(df.iloc[i].values[0])
            
        else: 

            exchange.append(df.iloc[i].values[0])
            
    new_df = pd.DataFrame({
        "date": date, 
        "exchange_rate": exchange
    })

    ## Dropping the last row 

    new_df.drop(new_df.tail(1).index, inplace=True)

    ## Removing the square brackets 
    # Function to clean exchange_rate column
    def clean_exchange_rate(rate):
        # Split the rate by space and remove duplicates
        parts = rate.split()
        seen = set()
        unique_parts = []
        for part in parts:
            if part not in seen:
                unique_parts.append(part)
                seen.add(part)
        # Join the unique parts back into a single string
        return ' '.join(unique_parts)

    # Apply the cleaning function to the exchange_rate column
    new_df['exchange_rate'] = new_df['exchange_rate'].apply(clean_exchange_rate)

    # Further split and clean the date column if necessary
    def clean_date(date):
        parts = date.split()
        # Assuming the first three parts represent the full date in text form
        clean_date = ' '.join(parts[:3])
        return clean_date

    new_df['date'] = new_df['date'].apply(clean_date)


    
    ## Converting the exchange rate column 
    
    # I will need to find the row number and delete it 
    
    # Finding the row 
    row_number = new_df[new_df.date == "Worst IDR to"].index 
    
    
  

    new_df.drop(row_number, axis=0, inplace=True)

  

    # Apply the extraction function to the exchange_rate column
    
    
    
    ## Applying the datetime 
    new_df.index = pd.to_datetime(new_df.date) 
    new_df.drop('date', axis=1, inplace=True)
    
    def extract_exchange_rate(rate):
    # Split the rate by space and take the 4th part which is the numeric value
        parts = rate.split()
        return float(parts[3])

    new_df['exchange_rate'] = new_df.exchange_rate.apply(extract_exchange_rate)
    
    new_df.rename({"exchange_rate": "pounds_in_a_rupiah"}, axis=1, inplace=True)
    new_df['rupiahs_in_a_pound'] = 1 / new_df.pounds_in_a_rupiah    
    print (f"{year} data: done")
    # I will need to combine all the data together
    
    
    
    return new_df







# the data should be from 2015 onwards 



# I need to call the second function

################################################
## The problem lays in the algorithm below:
years = {}
for i in range(min_year, max_year + 1):
    year_key = f"{i}"  # Create a dynamic key name
    years[year_key] = collect_data(i)  # Assign a value to the dictionary

print(years)

# I can write this into a .csv file before loading into a website

array = [years[i] for i in years.keys()]
df = pd.concat([*array], axis=0)


print ("---------------------------")

print ("results:") 

print (max(df.index))
print (min_year)
print (max_year) 

year_2024 = collect_data(2024)


