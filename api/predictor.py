from datetime import datetime
from .models import *
import pandas as pd


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WeatherPredictor(metaclass=Singleton):
    def __init__(self):
        self.temp_predictor = TemperaturePredictor()
        self.humidity_predictor = HumidityPredictor()
        self.pressure_predictor = PressurePredictor()
        self.rain_classifier = RainClassifier()

    def forecast_temperature(self, timestamp, location):
        predicted = self.temp_predictor.forecast(timestamp)
        predicted.index.strftime("%Y-%m-%d %H:%M:%S")
        return (
            predicted.rename("temperature")
            .reset_index()
            .rename(columns={"index": "ts"})
            .to_dict(orient="records")
        )

    def forecast_humidity(self, timestamp, location):
        date = datetime.strptime(timestamp, "%Y/%m/%d %H:%M")
        if self.get_hour_difference(datetime.now(), date) <= 24:
            temp = self.forecast_temperature(timestamp, location)
            pressure = self.forecast_pressure(timestamp, location)
            exog = pd.merge(temp, pressure, left_index=True, right_index=True)
            predicted = self.humidity_predictor.forecast_detailed(timestamp, exog)
            predicted.index.strftime("%Y-%m-%d %H:%M:%S")
            return (
                predicted.rename("humidity")
                .reset_index()
                .rename(columns={"index": "ts"})
                .to_dict(orient="records")
            )

        predicted = self.humidity_predictor.forecast(timestamp)
        predicted.index.strftime("%Y-%m-%d %H:%M:%S")
        return (
            predicted.rename("humidity")
            .reset_index()
            .rename(columns={"index": "ts"})
            .to_dict(orient="records")
        )

    def forecast_pressure(self, timestamp, location):
        predicted = self.pressure_predictor.forecast(timestamp)
        predicted.index.strftime("%Y-%m-%d %H:%M:%S")
        return (
            predicted.rename("pressure")
            .reset_index()
            .rename(columns={"index": "ts"})
            .to_dict(orient="records")
        )

    def forecast_rain(self, weather_data):
        predicted = self.rain_classifier.classify(weather_data)
        return [{"weather": item} for item in predicted]

    @staticmethod
    def get_hour_difference(start_date: datetime, end_date: datetime):
        time_diff = abs(end_date - start_date)
        return time_diff.seconds // 360
