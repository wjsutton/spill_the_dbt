import requests
import pandas as pd
import duckdb

def fetch_weather_data(latitude, longitude):
    """
    Fetches the current weather data from the Open-Meteo API for the given latitude and longitude.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data

def flatten_weather_data(data, office_name):
    """
    Parses and flattens the JSON data into a Pandas DataFrame and adds the office name.
    """
    # Extract 'current_weather' data
    current_weather = data.get('current_weather', {})
    df_current = pd.DataFrame([current_weather])

    # Add additional data from the top-level JSON
    additional_data = {
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'elevation': data.get('elevation'),
        'timezone': data.get('timezone'),
        'generationtime_ms': data.get('generationtime_ms'),
        'utc_offset_seconds': data.get('utc_offset_seconds'),
        'office': office_name  # Add the office name
    }
    for key, value in additional_data.items():
        df_current[key] = value

    return df_current

def load_data_to_duckdb(df):
    """
    Loads the DataFrame into a DuckDB table.
    """
    con = duckdb.connect('requirements/ch03_data/office_weather.db')
    con.execute("CREATE TABLE IF NOT EXISTS weather_data AS SELECT * FROM df LIMIT 0")
    con.execute("INSERT INTO latest_weather_readings SELECT * FROM df")
    con.close()


# Read office locations from CSV
office_df = pd.read_csv('requirements/ch03_data/office_locations.csv')

# Initialize an empty list to collect DataFrames
df_list = []

# Loop through each office and fetch weather data
for office_name, latitude, longitude in zip(office_df['office'], office_df['lat'], office_df['long']):
    print(f"Fetching data for {office_name} ({latitude}, {longitude})...")
    data = fetch_weather_data(latitude, longitude)
    df = flatten_weather_data(data, office_name)
    df_list.append(df)

# Combine all DataFrames into one
all_data_df = pd.concat(df_list, ignore_index=True)

# Load the combined DataFrame into DuckDB
load_data_to_duckdb(all_data_df)
print("All data has been successfully loaded into DuckDB.")
