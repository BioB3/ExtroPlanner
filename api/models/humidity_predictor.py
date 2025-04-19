from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from .abstract_predictor import AbstractPredictor
import os


class HumidityPredictor(AbstractPredictor):

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, 'trained_models',
                                 'humidity_SARIMA.pkl')
        self.sarima = SARIMAXResults.load(model_dir)

        model_dir = os.path.join(current_dir, 'trained_models',
                                 'humidity_SARIMAX.pkl')
        self.sarimax = SARIMAXResults.load(model_dir)

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def forecast_detailed(self, timestamp, exog):
        return self.sarimax.forecast(steps=timestamp, exog=exog)

    def refit(self, data):
        pass

    def retrain(self, data):
        pass
