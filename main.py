from fastapi import FastAPI

from PyQt5.QtWidgets import  QApplication,QMainWindow , QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor , QPixmap
from datetime import datetime, timedelta
import requests
import pprint

import sys
from PyQt5.QtCore import Qt

from app import schemas
from app.ui.ui_weather import Ui_MainWindow
from app.routers import weather

# Create a FastAPI instance
app = FastAPI()

origins = ["*"]
#is typically used in the context of configuring Cross - Origin Resource Sharing(CORS)
# for a web server or application.
# CORS is a security feature implemented by web browsers to control how web pages in one domain can request
# and interact with resources from another domain.

API_KEY = "f002c9a8e241b7fceebea7741c486e8b"

app.include_router(weather.router)

@app.get("/")
def index():
    return {"message": "Hello ٌWeather!"}


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,120))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.get_current_weather()
        self.get_5days_weather(35.68,51.38)
        self.get_6hours_later_weather(35.68,51.38)

    def get_current_weather(self):
        city = self.ui.city_line_edt.text()
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        weather_data = requests.get(base_url).json()
        # Access the weather icon
        weather_icon = weather_data['weather'][0]['icon']
        pixmap = QPixmap(f":/images/images/{weather_icon}.png")  # Replace 'your_image.png' with your image path
        label_width = self.ui.current_icon_label.width()
        label_height = self.ui.current_icon_label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
        self.ui.current_icon_label.setPixmap(pixmap)
        #temp and weather_type
        self.ui.current_temp_label.setText(f"{weather_data['main']['temp']}ºC")
        self.ui.current_weathertype_label.setText(f"{weather_data['weather'][0]['description'].lower().title()}")
        #date
        timestamp= weather_data['dt']
        dt = datetime.fromtimestamp(timestamp)
        self.ui.current_date_label.setText(dt.strftime("%A, %d %B %Y"))
        #lat , lang
        latitude = weather_data["coord"]["lat"]
        longitude = weather_data["coord"]["lon"]
        self.get_5days_weather(35.68,51.38)

    def get_5days_weather(self, latitude, longitude):
        base_url = "http://localhost:8000"  # Replace with the actual URL
        response = requests.get(f"{base_url}/weather/future_days_weather/{latitude}/{longitude}")

        if response.status_code == 200:
            weather_data = response.json()
            # The 'weather_data' variable now contains the response from your FastAPI endpoint.
            print(weather_data)
            daily_weather_data = []

        #-------------------------------------------------------------------
            counter = 1
            for entry in weather_data:
                if counter<6:
                    day_name = f"day_label_{counter}"
                    # getattr() is used to access the label objects based on their dynamically constructed names
                    #date
                    future_day = getattr(self.ui, day_name)
                    date = entry['date']
                    future_day.setText(date)
                    #temp
                    weather_degree = f"day_temp_label_{counter}"
                    weather_temp = getattr(self.ui, weather_degree)
                    weather_temp.setText(entry['temp'])
                    #icon
                    weather_icon_lbl = f"day_icon_label_{counter}"
                    icon = getattr(self.ui, weather_icon_lbl)
                    weather_icon = entry['icon']
                    pixmap = QPixmap(f":/images/images/{weather_icon}.png")  # Replace 'your_image.png' with your image path
                    icon_size = icon.size()
                    pixmap = pixmap.scaled(icon_size)
                    icon.setPixmap(pixmap)

                    counter = counter + 1
                else:
                    print(f"Request failed with status code {response.status_code}")


    def get_6hours_later_weather(self, lat, long):
        base_url = "http://localhost:8000"  # Replace with the actual URL
        response = requests.get(f"{base_url}/weather/future_hours_weather/{lat}/{long}")

        if response.status_code == 200:
            weather_data = response.json()
            # The 'weather_data' variable now contains the response from your FastAPI endpoint.
            pprint.pprint(weather_data)

            counter = 1
            for entry in weather_data:
                if counter < 6:
                    time_label = f"time_label_{counter}"
                    # getattr() is used to access the label objects based on their dynamically constructed names
                    future_time = getattr(self.ui, time_label)
                    time_value = entry['time']
                    future_time.setText(time_value)

                    weather_degree = f"degree_label_{counter}"
                    # # getattr() is used to access the label objects based on their dynamically constructed names
                    weather_temp = getattr(self.ui, weather_degree)
                    # weather_temp.setText(f"{((float(entry['temp'])) -273.15):.0f} ºC")
                    weather_temp.setText(entry['temp'])

                    weather_icon_lbl = f"time_icon_label_{counter}"
                    icon = getattr(self.ui, weather_icon_lbl)
                    weather_icon = entry['icon']
                    pixmap = QPixmap(
                        f":/images/images/{weather_icon}.png")  # Replace 'your_image.png' with your image path
                    label_width = icon.width()
                    label_height = icon.height()
                    pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
                    icon.setPixmap(pixmap)

                    counter = counter + 1
        else:
            print("Error: Unable to fetch weather data.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
