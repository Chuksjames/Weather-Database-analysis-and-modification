# Author: <Chukwuma James Okafor>
# Student ID: <D3041895>

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import sqlite3

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Middlesbrough

# The order of variables daily is assigned correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": -1.23483,
    "longitude": 54.57623,
    "start_date": "2023-01-01",
    "end_date": "2023-12-27",
    "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_sum"]
}
responses = openmeteo.weather_api(url, params=params)

# SQLite database connection
db_path = "..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Process daily data. 
daily = responses[0].Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()

daily_data = {
    'city_id' : 1,
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    ),
    "max_temp": daily_temperature_2m_max.round(1),
    "min_temp": daily_temperature_2m_min.round(1),
    "mean_temp": daily_temperature_2m_mean.round(1),
    "precipitation": daily_precipitation_sum.round(1)
}

daily_dataframe = pd.DataFrame(data=daily_data)

# Insert data into SQLite database
daily_dataframe.to_sql("daily_weather_entries", connection, if_exists='append', index=False)

# Close database connection
connection.close()

# Print the resulting DataFrame with one decimal place
pd.set_option('display.float_format', '{:.1f}'.format)
print(daily_dataframe)


