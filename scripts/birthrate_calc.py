import sqlite3
import pandas as pd


def load_data_for_year(year, db_path='data/world_birth_data.db'):
    """
    Load birth rate and population data for a given year from the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT Country, Birth_Rate_per_1000, Population
        FROM birth_population
        WHERE Year = {year}
    """
    df_year = pd.read_sql(query, conn)
    conn.close()
    return df_year


def calculate_birth_probability(df, country='Canada'):
    """
    Calculate the probability of being born in the specified country
    compared to total global births.
    """
    df['Total_Births'] = (df['Birth_Rate_per_1000'] / 1000) * df['Population']
    total_global_births = df['Total_Births'].sum()

    country_row = df[df['Country'] == country]
    if country_row.empty:
        raise ValueError(f"No data available for country '{country}'")

    country_births = country_row['Total_Births'].values[0]
    probability = (country_births / total_global_births) * 100
    return probability, total_global_births, country_births
