import requests
from datetime import datetime
import pymysql
import json

with open("config.json", "r") as f:
    config = json.load(f)

endpoint = config["endpoint"]
username = config["username"]
password = config["password"]
database_name = config["database_name"]


connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)


def main():
    response = requests.get('https://goboardapi.azurewebsites.net/api/FacilityCount/GetCountsByAccount?AccountAPIKey=7938FC89-A15C-492D-9566-12C961BC1F27')

    response_json = response.json()

    locations = [13, 12, 9, 16] 
    names = ['Lvl1', 'Lvl2', 'Lvl3', 'PowerHouse']

    for i in range(len(locations)):
        location_dict = response_json[locations[i]]
    
        # Percent Capacity
        max_capacity = location_dict['TotalCapacity']
        population = location_dict['LastCount']
        percent_capacity = round(population / max_capacity * 100, 2)

        # Time of Day
        str_time = location_dict['LastUpdatedDateAndTime']

        date_time = datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S.%f')

        hour = date_time.strftime("%H")
        minute = date_time.strftime('%M')

        # Month
        month_number = int(date_time.strftime("%m"))
        month_word = date_time.strftime("%B")

        # Weekday
        weekday_number = int(date_time.strftime("%w"))
        weekday_word = date_time.strftime("%A")

        # Year
        year = int(date_time.strftime("%Y"))


        # Export data to MySQL database
        cursor = connection.cursor()

        cursor.execute(f'INSERT INTO {names[i]} (Population, Percent_Capacity, Hour, Minute, Weekday, Weekday_Word, Month, Month_Word, Year) values ' 
                       f'({population}, {percent_capacity}, {hour}, {minute}, {weekday_number}, "{weekday_word}", {month_number}, "{month_word}", {year})')
        
        connection.commit()


def handler(event, context):
    main()