import requests
import pandas as pd
import sqlite3
# import os

# Function to fetch World Bank data, given an indicator
def fetch_world_bank_data(indicator):
    """
    Fetch data from the World Bank API for a given indicator.
    Returns a pandas DataFrame with columns: Country, ISO3, Year, <indicator>.
    """
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=30000"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()[1]  # [0] is metadata, [1] is data
    df = pd.json_normalize(data)
    df = df[['country.value', 'countryiso3code', 'date', 'value']]
    df.rename(columns={
        'country.value': 'Country',
        'countryiso3code': 'ISO3',
        'date': 'Year',
        'value': indicator
    }, inplace=True)
    return df

# Function to fetch, process, and store the data
def fetch_and_store_data(db_path='data/world_birth_data.db'):
    """
    Fetch birth rate and population data from World Bank,
    merge them, clean them, and store in an SQLite database.
    """
    # os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Fetching the data
    birth_rate_df = fetch_world_bank_data('SP.DYN.CBRT.IN')
    population_df = fetch_world_bank_data('SP.POP.TOTL')

    # Merging dataframes on common columns
    merged_df = pd.merge(birth_rate_df, population_df, on=['Country', 'ISO3', 'Year'])
    merged_df.rename(columns={
        'SP.DYN.CBRT.IN': 'Birth_Rate_per_1000',
        'SP.POP.TOTL': 'Population'
    }, inplace=True)

    # Cleaning the Data
    merged_df.dropna(subset=['Birth_Rate_per_1000', 'Population'], inplace=True)
    merged_df['Year'] = merged_df['Year'].astype(int)
    merged_df['Birth_Rate_per_1000'] = merged_df['Birth_Rate_per_1000'].astype(float)
    merged_df['Population'] = merged_df['Population'].astype(int)

    # Save the dataframe to SQLite database
    conn = sqlite3.connect(db_path)
    merged_df.to_sql('birth_population', conn, if_exists='replace', index=False)
    conn.close()

    print(f"[Success] Data successfully stored in {db_path}")

def load_merged_data(db_path='data/world_birth_data.db'):
    """
    Load the merged birth and population data from the SQLite database.
    Returns a pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM birth_population", conn)
    conn.close()
    return df