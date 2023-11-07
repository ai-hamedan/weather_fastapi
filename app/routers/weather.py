from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import APIRouter#........
# from sqlalchemy.orm import Session
from typing import List, Optional
import requests
from datetime import datetime, timedelta
import pprint

from .. import schemas
router = APIRouter(
    prefix="/weather",
    tags=['Weather']
)

# @router.get("/future_days_weather/{lat}/{long}", response_model=[schemas.FutureDaysWeather])
@router.get("/future_days_weather/{lat}/{long}")
def get_future_days_weather(lat:float, long:float):
    try:
        API_KEY = "f002c9a8e241b7fceebea7741c486e8b"
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        print(data)
        # For example, you can create a list of schemas.FutureDaysWeather objects from the data
        future_days_weather:schemas.FutureDaysWeather = []

        for entry in data['list']:
            dt_txt = entry['dt_txt']
            day_hour = dt_txt.split(" ")
            day = datetime.strptime(day_hour[0], "%Y-%m-%d").date()
            w_time = datetime.strptime(day_hour[1], "%H:%M:%S").time()

            noon = datetime.strptime("12:00:00", "%H:%M:%S").time()
            if w_time == noon:
                future_days_weather.append({
                    'date': day.strftime('%A'),
                    'temp': f"{(entry['main']['temp'] - 273.15):.0f} ºC",
                    'icon': entry['weather'][0]['icon']
                })

        return future_days_weather
        # return data
    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors
        return {"error": "Request to the weather API failed."}

@router.get("/future_hours_weather/{lat}/{long}")
def get_future_hours_weather(lat:float, long:float):
    # try:
    #   API_KEY = "f002c9a8e241b7fceebea7741c486e8b"
    #     url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={API_KEY}"
    #     response = requests.get(url)
    #     data = response.json()
    #     print(data)
    #     # For example, you can create a list of schemas.FutureDaysWeather objects from the data

    API_KEY = "f002c9a8e241b7fceebea7741c486e8b"

    # Make the API request to get the hourly forecast data
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract the hourly forecast data... 'list' is the part of the data that we need
        hourly_forecast = data["list"]

        future_hours_weather: schemas.FutureHoursWeather = []
        # Find the forecast data for the desired time
        counter = 0
        for hour_data in hourly_forecast:
            forecast_time = datetime.strptime(hour_data["dt_txt"], '%Y-%m-%d %H:%M:%S')
            if (counter < 5):
                if (forecast_time > datetime.now()):
                    future_hours_weather.append({
                        # 'time': forecast_time.time(),  # the format is: '2023-10-26T21:30:00'
                        'time': forecast_time.strftime('%H:%M'),  # the format is: '2023-10-26T21:30:00'
                        'temp': f"{(hour_data['main']['temp'] - 273.15):.0f} ºC",
                        'icon': hour_data['weather'][0]['icon']
                    })
                    counter = counter + 1
        pprint.pprint(future_hours_weather)
        return future_hours_weather
    else:
        print("Error: Unable to fetch weather data.")









        # if response.status_code == 200:
        #     data = response.json()
        #
        #     # Extract the hourly forecast data... 'list' is the part of the data that we need
        #     hourly_forecast = data["list"]
        #
        #     future_hours_weather: schemas.FutureHoursWeather = []
        #     # Find the forecast data for the desired time
        #     for hour_data in hourly_forecast:
        #         forecast_time = datetime.fromtimestamp(hour_data["dt"])
        #         if forecast_time <= target_time:
        #             future_hours_weather.append({
        #                 'time': forecast_time.split('T')[1], # the format is: '2023-10-26T21:30:00'
        #                 'temp': f"{(hour_data['main']['temp'] - 273.15):.0f} ºC",
        #                 'icon': hour_data['weather'][0]['icon']
        #             })
        #             # weather_description = hour_data["weather"][0]["description"]
        #             # print(
        #             #     f"Weather at {forecast_time}: {weather_description}")  # Weather at 2023-10-18 00:30:00: clear sky
        #             # break
        # else:
        #     print("Error: Unable to fetch weather data.")

        # future_days_weather: FutureDaysWeather = []
        # for entry in data['list']:
        #     dt_txt = entry['dt_txt']
        #     day_hour = dt_txt.split(" ")
        #
        #     day = datetime.strptime(day_hour[0], "%Y-%m-%d").date()
        #     w_time = datetime.strptime(day_hour[1], "%H:%M:%S").time()
        #     noon = datetime.strptime("12:00:00", "%H:%M:%S").time()
        #     if w_time == noon:
        #         future_days_weather.append({
        #             'date': day.strftime('%A'),
        #             'temp': f"{(entry['main']['temp'] - 273.15):.0f} ºC",
        #
        #             'icon': entry['weather'][0]['icon']
        #         })
        return future_hours_weather

    # return data
    # except requests.exceptions.RequestException as e:
    #  # Handle HTTP request errors
    #     return {"error": "Request to the weather API failed."}

