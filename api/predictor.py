from datetime import datetime
from models import *
import pandas as pd


class WeatherPredictor:
    def __init__(self):
        self.temp_predictor = TemperaturePredictor()
        self.humidity_predictor = HumidityPredictor()
        self.pressure_predictor = PressurePredictor()
        self.rain_classifier = RainClassifier()

    def forecast_temperature(self, timestamp, location):
        return self.temp_predictor.forecast(timestamp)

    def forecast_humidity(self, timestamp, location):
        date = datetime.fromisoformat(timestamp)
        if self.get_hour_difference(datetime.now(), date) <= 24:
            temp = self.forecast_temperature(timestamp, location)
            pressure = self.forecast_pressure(timestamp, location)
            exog = pd.merge(temp, pressure, left_index=True, right_index=True)
            return self.humidity_predictor.forecast_detailed(timestamp, exog)
        return self.humidity_predictor.forecast(timestamp)

    def forecast_pressure(self, timestamp, location):
        return self.pressure_predictor.forecast(timestamp)

    def forecast_rain(self, weather_data):
        return self.rain_classifier.classify(weather_data)

    @staticmethod
    def get_hour_difference(start_date: datetime, end_date: datetime):
        time_diff = abs(end_date - start_date)
        return time_diff.seconds // 360
