# Author: <Chukwuma James Okafor>
# Student ID: <D3041895>

import phase_1
import phase_2
import sqlite3

def menu(connection):

        while True:
            print ("1. print all cities")
            print ("2. print all countries")
            print ("3. print average_annual_temperature")
            print ("4. print average_seven_day_precipitation")
            print ("5. print average_mean_temp_by_city")
            print ("6. print average_annual_precipitation_by_country")
            print ("7. plot_precipitation_bar_chart")
            print ("8. plot_grouped_precipitation_bar_chart_for_cities")
            print ("9. plot_average_annual_precipitation_by_country")
            print ("10. plot_min_max_mean_temp_and_precipitation_by_city")
            print ("11. plot_min_and_max_temp_by_city")
            print ("12. plot_scatter_chart")
            print ("13. plot_average_mean_temp_by_city")
            print ("14. Quit")

            choice = input("Your choice ? ")

            if choice == "1":
                phase_1.select_all_cities (connection)
            elif choice == "2":
                phase_1.select_all_countries (connection)
            elif choice == "3":
                phase_1.average_annual_temperature(connection, 1, 2020)
            elif choice == "4":
                phase_1.average_seven_day_precipitation(connection, 2, '2020-01-01')
            elif choice == "5":
                phase_1.average_mean_temp_by_city(connection, '2020-09-02', '2020-12-02')
            elif choice == "6":
                phase_1.average_annual_precipitation_by_country(connection, 2020)
            elif choice == "7":
                phase_2.plot_precipitation_bar_chart(connection, 1, '2020-01-01')
            elif choice == "8":
                phase_2.plot_grouped_precipitation_bar_chart_for_cities(connection, [1, 2, 3, 4], '2020-01-01')
            elif choice == "9":
                phase_2.plot_average_annual_precipitation_by_country(connection, '2022')
            elif choice == "10":
                phase_2.plot_min_max_mean_temp_and_precipitation_by_city(connection, 2, 2020, 1)
            elif choice == "11":
                phase_2.plot_min_and_max_temp_by_city(connection, 1, 2020, 1)
            elif choice == "12":
                phase_2.plot_scatter_chart(connection, 'country')
            elif choice == "13":
                phase_2.plot_average_mean_temp_by_city(connection, '2020-01-01', '2020-12-31')           
            elif choice == "14":
                break
            else:
                print ("I don't recognise that option")

if __name__ == "__main__":
     pass
with sqlite3.Connection ("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
    menu(connection)
   
    


    






    
    
