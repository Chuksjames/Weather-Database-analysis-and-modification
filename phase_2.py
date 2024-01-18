# Author: <Chukwuma James Okafor>
# Student ID: <D3041895>

import sqlite3

# Phase 2 - Basic Graphs using Matplotlib

# Import library
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd


#1  Bar chart to show the 7-day precipitation for a specific town/city

def fetch_precipitation_data(connection, city_id, start_date):
    try:
        cursor = connection.cursor()

        # Use parameterized query to prevent SQL injection
        query = "SELECT date, precipitation FROM daily_weather_entries WHERE city_id = ? AND date BETWEEN ? AND date(?, '+6 days')"
        cursor.execute(query, (city_id, start_date, start_date))

        # Fetch all rows from the result
        rows = cursor.fetchall()

        return rows

    except Exception as e:
        print(f"Error fetching precipitation data: {e}")
        return None

def plot_precipitation_bar_chart(connection, city_id, start_date):
    data = fetch_precipitation_data(connection, city_id, start_date)

    if not data:
        print("No data found.")
        return

    dates, precipitation = zip(*data)

    plt.bar(dates, precipitation)
    plt.xlabel('Date')
    plt.ylabel('Precipitation')
    plt.title(f'7-Day Precipitation for City ID {city_id}')
    plt.show()


#2  Bar chart for a specified period for a specified set of towns/cities

def fetch_cities_precipitation_data(connection, city_ids, start_date):
    try:
        cursor = connection.cursor()

        # Use parameterized query to prevent SQL injection
        query = """
            SELECT c.name as city_name, d.date, d.precipitation
            FROM daily_weather_entries d
            JOIN cities c ON d.city_id = c.id
            WHERE d.city_id IN ({}) AND d.date BETWEEN ? AND date(?, '+6 days')
        """.format(','.join(['?']*len(city_ids)))

        cursor.execute(query, tuple(city_ids + [start_date, start_date]))

        # Fetch all rows from the result
        rows = cursor.fetchall()

        return rows

    except Exception as e:
        print(f"Error fetching precipitation data: {e}")
        return None

def plot_grouped_precipitation_bar_chart_for_cities(connection, city_ids, start_date):
    data = fetch_cities_precipitation_data(connection, city_ids, start_date)

    if not data:
        print("No data found.")
        return

    # Create a dictionary to store data for each city
    city_data = {city_name: {'dates': [], 'precipitation': []} for city_name in set(row[0] for row in data)}

    for row in data:
        city_name, date, precipitation = row[0], row[1], row[2]
        city_data[city_name]['dates'].append(date)
        city_data[city_name]['precipitation'].append(precipitation)

    # Plotting a grouped bar chart
    width = 0.2  # Width of the bars
    colors = ['b', 'g', 'r', 'c']  # Colors for each city

    ind = np.arange(len(city_data[list(city_data.keys())[0]]['dates']))  # X-axis positions for each group of bars

    for i, city_name in enumerate(city_data.keys()):
        plt.bar(ind + i * width, city_data[city_name]['precipitation'], width, label=f'{city_name}', color=colors[i])

    plt.xlabel('Date')
    plt.ylabel('Precipitation')
    plt.title(f'7-Day Precipitation for Cities {", ".join(map(str, city_data.keys()))}')
    plt.xticks(ind + width * (len(city_data) - 1) / 2, city_data[list(city_data.keys())[0]]['dates'])
    plt.legend()
    plt.show()


#3  Bar chart that shows the average yearly precipitation by country

def plot_average_annual_precipitation_by_country(connection, year):
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Define the query
        query = f"SELECT avg(precipitation) as avg_precipitation, cities.country_id FROM daily_weather_entries JOIN cities ON daily_weather_entries.city_id = cities.id WHERE date >= '{year}' GROUP BY country_id"
        
        # Execute the query via the cursor object
        results = cursor.execute(query)

        # Initialize lists to store country names and average precipitation values
        countries = []
        avg_precipitations = []

        # Iterate over the results and store data in lists
        for row in results:
            countries.append(row['country_id'])
            avg_precipitations.append(row['avg_precipitation'])

        # Plotting the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(countries, avg_precipitations, color='blue')
        plt.xlabel('Country ID')
        plt.ylabel('Average Precipitation')
        plt.title(f'Average Yearly Precipitation by Country ({year})')
        plt.show()

    except sqlite3.OperationalError as ex:
        print(ex)


#4  Grouped bar charts for displaying the min/max/mean temperature and precipitation values for selected cities or countries.

def plot_min_max_mean_temp_and_precipitation_by_city(connection, city_id, year, month):
    try:
        connection.row_factory = sqlite3.Row

        # Define the start and end dates for the selected month
        date_from = f'{year}-{month:02d}-01'
        date_to = f'{year}-{month:02d}-31'  # Assuming 31 days in a month

        # Join the tables to get weather information
        query = f"SELECT date, min_temp, max_temp, mean_temp, precipitation FROM daily_weather_entries WHERE city_id = {city_id} AND date >= '{date_from}' AND date <= '{date_to}'"
       
        # Execute the query
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetch the results
        rows = cursor.fetchall()

        dates = [row['date'] for row in rows]
        min_temps = [row['min_temp'] for row in rows]
        max_temps = [row['max_temp'] for row in rows]
        mean_temps = [row['mean_temp'] for row in rows]
        precipitation = [row['precipitation'] for row in rows]

        # Plotting grouped bar chart
        width = 0.2  # Adjust the width as needed
        plt.bar(dates, min_temps, width, label='Min Temp')
        plt.bar(dates, max_temps, width, label='Max Temp', bottom=min_temps)
        plt.bar(dates, mean_temps, width, label='Mean Temp', bottom=[sum(x) for x in zip(min_temps, max_temps)])
        plt.bar(dates, precipitation, width, label='Precipitation', bottom=[sum(x) for x in zip(min_temps, max_temps, mean_temps)])

        # Adding labels and title
        plt.xlabel('Date')
        plt.ylabel('Temperature and Precipitation')
        plt.title(f'Weather Information for City {city_id} - {year}-{month:02d}')

        # Adding legend
        plt.legend()

        # Display the plot
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

#5 	Multi-line chart to show the daily minimum and maximum temperature for a given month for a specific city

def plot_min_and_max_temp_by_city(connection, city_id, year, month):
    try:
        connection.row_factory = sqlite3.Row

        # Define the start and end dates for the selected month
        date_from = f'{year}-{month:02d}-01'
        date_to = f'{year}-{month:02d}-31'  # Assuming 31 days in a month

        # Define the query
        query = f"SELECT date, min_temp, max_temp FROM daily_weather_entries WHERE city_id = {city_id} AND date >= '{date_from}' AND date <= '{date_to}'"
        
        # Execute the query
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetch the results
        rows = cursor.fetchall()

        # Extract data for plotting
        dates = [row['date'] for row in rows]
        min_temps = [row['min_temp'] for row in rows]
        max_temps = [row['max_temp'] for row in rows]

        # Convert string dates to datetime objects for proper plotting
        dates = [mdates.datestr2num(date) for date in dates]

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot_date(dates, min_temps, '-o', label='Min Temperature')
        plt.plot_date(dates, max_temps, '-o', label='Max Temperature')

        # Formatting
        plt.title(f'Daily Min and Max Temperature for City {city_id} - {year}-{month:02d}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Show the plot
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


#6  Scatter plot chart for average temperature against average rainfall for town/city/country/all countries etc.

def get_average_weather_data(connection, group_by, filter_id=None):
    cursor = connection.cursor()

    # Construct the SQL query based on the specified group_by parameter
    if group_by == 'city':
        query = """
            SELECT city_id AS id, AVG(mean_temp) AS avg_temperature, AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries
            GROUP BY city_id
        """
        if filter_id:
            query += " HAVING city_id = ?"
            cursor.execute(query, (filter_id,))
        else:
            cursor.execute(query)
    elif group_by == 'country':
        query = """
            SELECT city_id, AVG(mean_temp) AS avg_temperature, AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries AS dwe
            JOIN cities ON dwe.city_id = cities.id
            GROUP BY cities.country_id
        """
        cursor.execute(query)
    elif group_by == 'all':
        query = """
            SELECT 'all' AS id, AVG(mean_temp) AS avg_temperature, AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries
        """
        cursor.execute(query)
    else:
        raise ValueError("Invalid group_by parameter. Supported values are 'city', 'country', or 'all'.")

    return cursor.fetchall()

def plot_scatter_chart(connection, group_by):
    # Retrieve data internally
    average_data = get_average_weather_data(connection, group_by, filter_id=None)

    # Convert the data to a Pandas DataFrame for easier manipulation
    df = pd.DataFrame(average_data, columns=['id', 'avg_temperature', 'avg_precipitation'])
    
    # Create a scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter(df['avg_temperature'], df['avg_precipitation'], c='blue', alpha=0.7, edgecolors='w')

    # Customize the plot
    plt.xlabel('Average Temperature (°C)')
    plt.ylabel('Average Precipitation (units)')
    plt.title(f'Scatter Plot of Average Temperature vs Average Precipitation ({group_by.capitalize()})')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


#7  pie chart for average mean temperature by city

def plot_average_mean_temp_by_city(connection, date_from, date_to):
    try:
        connection.row_factory = sqlite3.Row

        # Define the query with a JOIN to get the city names
        query = f"""
            SELECT c.name, avg(d.mean_temp) as avg_temp
            FROM daily_weather_entries AS d
            JOIN cities AS c ON d.city_id = c.id
            WHERE d.date >= '{date_from}' AND d.date <= '{date_to}'
            GROUP BY d.city_id
        """
        print(query)

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        results = cursor.execute(query)

        # Store the results in a dictionary for plotting
        data = {}
        for row in results:
            city_name = row['name']
            avg_temp = row['avg_temp']
            data[city_name] = avg_temp

        if data:
            # Plotting a pie chart
            labels = list(data.keys())
            values = list(data.values())

            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title('Average Mean Temperature by City')
            plt.show()
        else:
            print("No data available for the specified date range.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    with sqlite3.Connection("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        cursor = connection.cursor()
    city_id = 1  # Replace with the desired city ID
    average_data = get_average_weather_data(connection, 'country', filter_id=None)

    plot_precipitation_bar_chart(connection, 1, '2020-01-01')
    plot_grouped_precipitation_bar_chart_for_cities(connection, [1, 2, 3, 4], '2020-01-01')
    plot_average_annual_precipitation_by_country(connection, '2022')
    plot_min_max_mean_temp_and_precipitation_by_city(connection, city_id, 2021, 2)
    plot_min_and_max_temp_by_city(connection, 1, 2020, 1)
    plot_scatter_chart(connection, 'country')
    plot_average_mean_temp_by_city(connection, '2020-01-01', '2020-12-31')


