from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from abstract_predictor import AbstractPredictor


class HumidityPredictor(AbstractPredictor):

    def __init__(self):
        self.sarima = SARIMAXResults.load('trained_models/humidity_SARIMA.pkl')
        self.sarimax = SARIMAXResults.load('trained_models/humidity_SARIMAX.pkl')

    def forecast(self, timestamp):
        return self.sarima.forecast(steps=timestamp)

    def forecast_detailed(self, timestamp, exog):
        return self.sarimax.forecast(steps=timestamp, exog=exog)

    def refit(self, data):
        pass

    def retrain(self, data):
        pass
