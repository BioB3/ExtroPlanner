from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from statsmodels.tsa.statespace.sarimax import SARIMAX
from .abstract_predictor import AbstractPredictor
import pandas as pd
import os


class HumidityPredictor(AbstractPredictor):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, "trained_models", "humidity_SARIMA.pkl")
        self.sarima = self.__get_model(SARIMAXResults.load(model_dir))

        model_dir = os.path.join(current_dir, "trained_models", "humidity_SARIMAX.pkl")
        self.sarimax = self.__get_model(SARIMAXResults.load(model_dir))

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def forecast_detailed(self, timestamp, exog):
        return self.sarimax.forecast(steps=timestamp, exog=exog)

    def refit(self, data):
        pass

    def retrain(self, data):
        pass

    def __get_model(self, saved_model) -> SARIMAXResults:
        order = saved_model.model.order
        seasonal_order = saved_model.model.seasonal_order
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "trained_models", "Kaset_train_data.csv")
        dataset = pd.read_csv(data_dir)
        model = SARIMAX(
            dataset.set_index("ts")["humidity"],
            order=order,
            seasonal_order=seasonal_order,
        )
        model = model.filter(saved_model.params)
        return model
