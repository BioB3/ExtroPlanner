from datetime import datetime
from datetime import timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm_api
from statsmodels.tsa.statespace.sarimax import SARIMAXResults


class WeatherPredictor:

    def forecast_temperature(self, timestamp, location):
        pass

    def forecast_humidity(self, timestamp, location):
        pass

    def forecast_pressure(self, timestamp, location):
        pass

    def forecast_rain(self, weather_data):
        pass

