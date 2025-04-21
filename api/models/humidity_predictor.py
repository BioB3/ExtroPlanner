from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from .abstract_predictor import AbstractPredictor
import pandas as pd
import os


class HumidityPredictor(AbstractPredictor):
    def __init__(self, location: str):
        self.last_obs = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, "trained_models", "humidity_SARIMA.pkl")
        self.sarima = self.__get_model(SARIMAXResults.load(model_dir), location)

        model_dir = os.path.join(current_dir, "trained_models", "humidity_SARIMAX.pkl")
        self.sarimax = self.__get_model(
            SARIMAXResults.load(model_dir), location, sarimax=True
        )

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def forecast_detailed(self, timestamp, exog):
        return self.sarimax.forecast(steps=timestamp, exog=exog)

    def refit(self, data):
        return self.sarima.append(data["humidity"])

    def __get_model(self, saved_model, location: str, sarimax=False) -> SARIMAXResults:
        order = saved_model.model.order
        seasonal_order = saved_model.model.seasonal_order
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(
            current_dir, "trained_models", "data", location + "_train_data.csv"
        )
        dataset = pd.read_csv(data_dir)
        self.last_obs = dataset.iloc[-1]["ts"]
        dataset["ts"] = pd.to_datetime(dataset["ts"])
        if sarimax:
            model = SARIMAX(
                dataset.set_index("ts")["humidity"].asfreq('30min'),
                exog=dataset.set_index("ts")[["temperature", "pressure"]].asfreq("30min"),
                order=order,
                seasonal_order=seasonal_order,
            )
            model = model.filter(saved_model.params)
            return model

        model = SARIMAX(
            dataset.set_index("ts")["humidity"].asfreq("30min"),
            order=order,
            seasonal_order=seasonal_order,
        )
        model = model.filter(saved_model.params)
        return model
