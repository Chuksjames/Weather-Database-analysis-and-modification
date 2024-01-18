# Author: <Chukwuma James Okafor>
# Student ID: <D3041895>

import sqlite3
import argparse

def average_mean_temp_by_city(connection, date_from, date_to):
    try:
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT avg(mean_temp) FROM daily_weather_entries WHERE date >= '{date_from}' AND date <= '{date_to}' GROUP BY city_id"
        print(query)

        # Get a cursor object from the database connection
        # that will be used to execute the database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"The average temperature by city: {row[0]:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)

def main():
    # Step 2: Create a parser object
    parser = argparse.ArgumentParser(description='Calculate average mean temperature by city within a date range.')

    # Step 3: Define arguments
    parser.add_argument('--date_from', default='2023-01-01', required=True)
    parser.add_argument('--date_to', default='2023-12-27', required=True)
   
    # Step 4: Parse the command-line arguments
    args = parser.parse_args()

    # Open a connection to your SQLite database
    with sqlite3.connect("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        # Call the function with the provided date range
        average_mean_temp_by_city(connection, args.date_from, args.date_to)

if __name__ == '__main__':
    main()


# Run the code below in the terminal
# python "Further Enhancements.py" --date_from "2023-01-01" --date_to "2023-12-27"





