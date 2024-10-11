
import requests
import pandas as pd

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
    current_weather = data.get('current_weather', {})
    df_current = pd.DataFrame([current_weather])

    additional_data = {
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'elevation': data.get('elevation'),
        'timezone': data.get('timezone'),
        'generationtime_ms': data.get('generationtime_ms'),
        'utc_offset_seconds': data.get('utc_offset_seconds'),
        'office': office_name
    }
    for key, value in additional_data.items():
        df_current[key] = value

    return df_current


def model(dbt, session):

    # Fetch office locations from the dbt seed
    office_df = dbt.ref('office_locations').to_df()

    df_list = []

    for office_name, latitude, longitude in zip(office_df['office'], office_df['lat'], office_df['long']):
        print(f"Fetching data for {office_name} ({latitude}, {longitude})...")
        data = fetch_weather_data(latitude, longitude)
        df = flatten_weather_data(data, office_name)
        df_list.append(df)

    all_data_df = pd.concat(df_list, ignore_index=True)

    return all_data_df

