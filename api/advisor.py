from datetime import datetime
from typing import Collection, Any
from .predictor import WeatherPredictor


class HeatIndexCalculator:
    __c1 = -8.78469475556
    __c2 = 1.61139411
    __c3 = 2.33854883889
    __c4 = -0.14611605
    __c5 = -0.012308094
    __c6 = -0.0164248277778
    __c7 = 2.211732e-3
    __c8 = 7.2546e-4
    __c9 = -3.582e-6

    @classmethod
    def calculate_heat_index(cls, t: float, h: float | int) -> float:
        """
        Return the calculated heat index

        Calculates a heat index using recorded temperature and
        relative humidity values.

        :param t: The temperature in Celsius
        :param h: The relative humidity in percentage
        :return: The calculated heat index in Celsius
        """
        return (
            cls.__c1
            + cls.__c2 * t
            + cls.__c3 * h
            + cls.__c4 * t * h
            + cls.__c5 * (t**2)
            + cls.__c6 * (h**2)
            + cls.__c7 * (t**2) * h
            + cls.__c8 * (h**2) * t
            + cls.__c9 * (h**2) * (t**2)
        )


class EventAdvisor:
    __rain_threshold = 0.8
    __heat_threshold = 0.8
    __heat_warn = 40.0
    __heat_danger = 45.0

    @classmethod
    def get_heat_index(cls, weather_data: Collection[dict[Any]]) -> list[float]:
        indexes = []
        for data in weather_data:
            heat_index = HeatIndexCalculator.calculate_heat_index(
                data["temperature"], data["humidity"]
            )
            indexes.append(heat_index)
        return indexes

    @classmethod
    def get_weather_conditions_summary(cls, weather_data):
        max_temp = max(weather_data, key=lambda x: x["temperature"])
        heat_indexes = cls.get_heat_index(weather_data)
        max_heat = max(heat_indexes)
        return {"max_temp": max_temp, "max_heat": max_heat}

    @classmethod
    def get_descriptive_event_advice(cls, weather_data):
        pass
