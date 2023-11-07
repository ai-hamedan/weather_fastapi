from datetime import datetime , date, time
from pydantic import BaseModel


# app = FastAPI()

#we have defined different models for different routes

class CurrentWeather(BaseModel):
    date: date
    time: time
    temp: float
    icon: bytes # ??????
    description: str


# Pydantic models for weather data
class FutureDaysWeather(BaseModel):
    date: date
    temp: float
    icon: bytes  # ??????

class FutureHoursWeather(BaseModel):
    time: time
    temp: float
    icon: bytes  # ??????


