import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAXResults, SARIMAX
from .abstract_predictor import AbstractPredictor
import os


class TemperaturePredictor(AbstractPredictor):
    def __init__(self, location: str):
        self.last_obs = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(
            current_dir, "trained_models", "temperature_SARIMA.pkl"
        )
        self.sarima = self.__get_model(SARIMAXResults.load(model_dir), location)

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def refit(self, data):
        return self.sarima.append(data["temperature"])

    def __get_model(self, saved_model, location: str) -> SARIMAXResults:
        order = saved_model.model.order
        seasonal_order = saved_model.model.seasonal_order
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(
            current_dir, "trained_models", "data", location + "_train_data.csv"
        )
        dataset = pd.read_csv(data_dir)
        self.last_obs = dataset.iloc[-1]["ts"]
        dataset["ts"] = pd.to_datetime(dataset["ts"])
        model = SARIMAX(
            dataset.set_index("ts")["temperature"].asfreq("30min"),
            order=order,
            seasonal_order=seasonal_order,
        )
        model = model.filter(saved_model.params)
        return model
