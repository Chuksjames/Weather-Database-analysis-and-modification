import unittest
import sqlite3

class TestWeatherFunctions(unittest.TestCase):

    def setUp(self):
        # Set up a SQLite3 connection for testing
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()

        # Create necessary tables and insert sample data for testing
        self.cursor.execute("CREATE TABLE countries (id INTEGER PRIMARY KEY, name TEXT, timezone TEXT)")
        self.cursor.execute("CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT, latitude REAL, longitude REAL, country_id INTEGER)")
        self.cursor.execute("CREATE TABLE daily_weather_entries (id INTEGER PRIMARY KEY, date TEXT, mean_temp REAL, precipitation REAL, city_id INTEGER)")

        self.cursor.execute("INSERT INTO countries (id, name, timezone) VALUES (1, 'Country1', 'UTC+1')")
        self.cursor.execute("INSERT INTO cities (id, name, latitude, longitude, country_id) VALUES (1, 'City1', 40.7128, -74.0060, 1)")
        self.cursor.execute("INSERT INTO daily_weather_entries (id, date, mean_temp, precipitation, city_id) VALUES (1, '2020-01-01', 15.0, 5.0, 1)")

        self.connection.commit()

    def tearDown(self):
        # Close the connection after each test
        self.connection.close()

    def select_all_countries(self, connection):
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
        
    def select_all_cities(self, connection):
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

    def average_annual_temperature(self, connection, city_id, year):
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

    def average_seven_day_precipitation(self, connection, city_id, start_date):
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

    def average_mean_temp_by_city(self, connection, date_from, date_to):
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

    def average_annual_precipitation_by_country(self, connection, year):
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

    def test_select_all_countries(self):
        self.select_all_countries(self.connection)

    def test_select_all_cities(self):
        self.select_all_cities(self.connection)

    def test_average_annual_temperature(self):
        self.average_annual_temperature(self.connection, 2, 2020)

    def test_average_seven_day_precipitation(self):
        self.average_seven_day_precipitation(self.connection, 2, '2020-01-01')

    def test_average_mean_temp_by_city(self):
        self.average_mean_temp_by_city(self.connection, '2020-09-02', '2020-12-02')

    def test_average_annual_precipitation_by_country(self):
        self.average_annual_precipitation_by_country(self.connection, 2020)

if __name__ == '__main__':
    unittest.main()
