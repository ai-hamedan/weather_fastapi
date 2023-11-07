from fastapi import FastAPI
from app.routers import weather

app = FastAPI()

# Include your FastAPI routers
app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

@app.get("/future_days_weather{lat,long}")
def get_future_days_weather(lat: float, long: float):

    return api.get_future_days_weather(lat, long)