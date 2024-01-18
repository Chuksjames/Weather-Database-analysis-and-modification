# Author: <Chukwuma James Okafor>
# Student ID: <D3041895>

import sqlite3

# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory
'''

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)

                    
def select_all_cities(connection):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = "SELECT * from [cities]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"City Id: {row['id']} -- City Name: {row['name']} -- City latitude: {row['latitude']} -- City longitude: {row['longitude']} -- country_id: {row['country_id']}")

    except sqlite3.OperationalError as ex:
        print(ex)


'''
Good
'''
def average_annual_temperature(connection, city_id, year):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT avg(mean_temp) from daily_weather_entries where date >= '{year}-01-01'  and date <= '{year}-12-31' and city_id = {city_id}"
        print(query)

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            if row[0] is not None:
                print(f"Average temperature was {round(row[0], 2)}")
            else:
                print("No temperature data available.")


    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(connection, city_id, start_date):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT avg(precipitation) FROM daily_weather_entries WHERE city_id = {city_id} AND date BETWEEN '{start_date}' AND date('{start_date}', '+6 days')"
        print(query)

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
                if row[0] is not None:
                    print(f"The average seven-day precipitation was {round(row[0], 2)}")
                else:
                    print("No precipitation data available.")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Very good
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT avg(mean_temp) from daily_weather_entries where date >= '{date_from}'  and date <= '{date_to}' group by city_id "
        print(query)

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"The average temperature by city: {row[0]:.2f}")
         
    except sqlite3.OperationalError as ex:
        print(ex)


def average_annual_precipitation_by_country(connection, year):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT avg(precipitation), cities.country_id from daily_weather_entries JOIN cities ON daily_weather_entries.city_id = cities.id WHERE date >= '{year}' group by country_id"
        print(query)
        # date difference = 7 days

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"The average precipitation by country: {row[0]:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)


'''
Excellent

You have gone beyond the basic requirements for this aspect.

'''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    pass

with sqlite3.Connection("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
    cursor = connection.cursor()
    
    cities = cursor.execute("")

    select_all_countries(connection)
    select_all_cities(connection)
    average_annual_temperature(connection, 2, 2020)
    average_seven_day_precipitation(connection, 2, '2020-01-01')
    average_mean_temp_by_city(connection, '2020-09-02', '2020-12-02')
    average_annual_precipitation_by_country(connection, 2020)
