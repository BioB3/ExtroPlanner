from datetime import datetime
from .models import *
import pandas as pd
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class WeatherPredictor(metaclass=Singleton):
    def __init__(self, db_connection):
        self.temp_predictors = {}
        self.humidity_predictors = {}
        self.pressure_predictors = {}
        self.rain_classifier = RainClassifier()
        self.__db = db_connection

    @staticmethod
    def get_valid_predictor_locations():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        location_data = os.listdir(
            os.path.join(current_dir, "models", "trained_models", "data")
        )
        locations = [entry.split("_train_data.csv")[0] for entry in location_data]
        return locations

    def get_humidity_predictor(self, location):
        if location in self.humidity_predictors:
            return self.humidity_predictors[location]

        self.humidity_predictors[location] = HumidityPredictor(location)
        return self.humidity_predictors[location]

    def get_temperature_predictor(self, location):
        if location in self.temp_predictors:
            return self.temp_predictors[location]

        self.temp_predictors[location] = TemperaturePredictor(location)
        return self.temp_predictors[location]

    def get_pressure_predictor(self, location):
        if location in self.pressure_predictors:
            return self.pressure_predictors[location]

        self.pressure_predictors[location] = PressurePredictor(location)
        return self.pressure_predictors[location]

    def forecast_temperature(self, timestamp, location):
        predicted = self.get_temperature_predictor(location).forecast(timestamp)
        predicted.index.strftime("%Y-%m-%d %H:%M:%S")
        return (
            predicted.rename("temperature")
            .reset_index()
            .rename(columns={"index": "ts"})
            .to_dict(orient="records")
        )

    def forecast_humidity(self, timestamp, location):
        date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        if self.get_hour_difference(datetime.now(), date) <= 24:
            temp = self.get_temperature_predictor(location).forecast(timestamp)
            pressure = self.get_pressure_predictor(location).forecast(timestamp)
            exog = pd.merge(temp, pressure, left_index=True, right_index=True)
            predicted = self.get_humidity_predictor(location).forecast_detailed(
                timestamp, exog
            )
            predicted.index.strftime("%Y-%m-%d %H:%M:%S")
            return (
                predicted.rename("humidity")
                .reset_index()
                .rename(columns={"index": "ts"})
                .to_dict(orient="records")
            )

        predicted = self.get_humidity_predictor(location).forecast(timestamp)
        predicted.index.strftime("%Y-%m-%d %H:%M:%S")
        return (
            predicted.rename("humidity")
            .reset_index()
            .rename(columns={"index": "ts"})
            .to_dict(orient="records")
        )

    def forecast_pressure(self, timestamp, location):
        predicted = self.get_pressure_predictor(location).forecast(timestamp)
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
