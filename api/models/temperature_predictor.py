from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from .abstract_predictor import AbstractPredictor
import os


class TemperaturePredictor(AbstractPredictor):

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, 'trained_models', 'temperature_SARIMA.pkl')
        self.sarima = SARIMAXResults.load(model_dir)

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def refit(self, data):
        pass

    def retrain(self, data):
        pass
