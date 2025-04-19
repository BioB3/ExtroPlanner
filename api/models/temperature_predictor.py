from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from abstract_predictor import AbstractPredictor


class TemperaturePredictor(AbstractPredictor):

    def __init__(self):
        self.sarima = SARIMAXResults.load('trained_models/temperature_SARIMA.pkl')

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def refit(self, data):
        pass

    def retrain(self, data):
        pass
