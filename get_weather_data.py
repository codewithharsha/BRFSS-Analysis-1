import os
import requests
import json
import csv
from datetime import datetime, timedelta

# Check if the file already exists
if not os.path.exists('weather_data.csv'):
    # Define API key and base URL
    API_KEY = "d4175b0c17b641b3ba442529252204"
    BASE_URL = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"

    # Define states
    states = {
        1: "Alabama", 2: "Alaska", 4: "Arizona", 5: "Arkansas", 6: "California", 8: "Colorado",
        9: "Connecticut", 10: "Delaware", 11: "District of Columbia", 12: "Florida", 13: "Georgia",
        15: "Hawaii", 16: "Idaho", 17: "Illinois", 18: "Indiana", 19: "Iowa", 20: "Kansas",
        22: "Louisiana", 23: "Maine", 24: "Maryland", 25: "Massachusetts", 26: "Michigan",
        27: "Minnesota", 28: "Mississippi", 29: "Missouri", 30: "Montana", 31: "Nebraska",
        32: "Nevada", 33: "New Hampshire", 34: "New Jersey", 35: "New Mexico", 36: "New York",
        37: "North Carolina", 38: "North Dakota", 39: "Ohio", 40: "Oklahoma", 41: "Oregon",
        44: "Rhode Island", 45: "South Carolina", 46: "South Dakota", 47: "Tennessee", 48: "Texas",
        49: "Utah", 50: "Vermont", 51: "Virginia", 53: "Washington", 54: "West Virginia",
        55: "Wisconsin", 56: "Wyoming", 66: "Guam", 72: "Puerto Rico", 78: "Virgin Islands"
    }

    # Define date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    # Create CSV file
    with open('weather_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['State', 'Date', 'Temperature (C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Weather Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for state_id, state_name in states.items():
            params = {
                "q": state_name,
                "date": start_date.strftime('%Y-%m-%d'),
                "enddate": end_date.strftime('%Y-%m-%d'),
                "tp": "24",
                "format": "json",
                "key": API_KEY
            }

            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if 'data' in data and 'weather' in data['data']:
                for weather_data in data['data']['weather']:
                    writer.writerow({
                        'State': state_name,
                        'Date': weather_data['date'],
                        'Temperature (C)': weather_data['avgtempC'],
                        'Wind Speed (km/h)': weather_data.get('hourly', [{}])[0].get('windspeedKmph', ''),
                        'Humidity (%)': weather_data.get('hourly', [{}])[0].get('humidity', ''),
                        'Weather Type': weather_data.get('hourly', [{}])[0].get('weatherDesc', [''])[0]['value']
                    })
            else:
                print(f"No weather data found for {state_name}")

    print("Weather data CSV file generated successfully.")
else:
    print("weather_data.csv already exists. Skipping download.")
