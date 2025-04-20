import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAXResults, SARIMAX
from .abstract_predictor import AbstractPredictor
import os


class TemperaturePredictor(AbstractPredictor):
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(
            current_dir, "trained_models", "temperature_SARIMA.pkl"
        )
        self.sarima = self.__get_model(SARIMAXResults.load(model_dir))

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

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
            dataset.set_index("ts")["temperature"],
            order=order,
            seasonal_order=seasonal_order,
        )
        model = model.filter(saved_model.params)
        return model
