import unittest
from enum import Enum
from collections.abc import Collection
from fastapi.testclient import TestClient
from api.app import app_api
from datetime import datetime

MOCK_AGGREGATE_DATA = [
    ("2025-04-07T00:00:00", "Kasetsart University", 3.524374946951866, 3.625, 1011.2083333333334, 30.733750065167744, 73.39583333333333, 33.9375, 3.4799999594688416, "few clouds,light rain,moderate rain,overcast clouds,scattered clouds"),
    ("2025-04-08T00:00:00", "Kasetsart University", 2.6402082641919455, 2.8125, 1011.6666666666666, 31.11020827293396, 72.9375, 30.333333333333332, 0, "broken clouds,few clouds,overcast clouds,scattered clouds"),
    ("2025-04-09T00:00:00", "Kasetsart University", 3.337692242402297, 3.5128, 1009.7435897435897, 31.88974331586789, 70.82051282051282, 20, 0, "few clouds"),
    ("2025-04-10T00:00:00", "Kasetsart University", 2.9944999516010284, 3.1, 1007.85, 31.172000026702882, 82.175, 44.95, 1.179999977350235, "broken clouds,few clouds,light rain,overcast clouds,scattered clouds"),
    ("2025-04-11T00:00:00", "Kasetsart University", 3.268958275516828, 3.4583, 1007.2083333333334, 30.160624941190083, 81.39583333333333, 26.666666666666668, 0, "few clouds,scattered clouds"),
    ("2025-04-12T00:00:00", "Kasetsart University", 2.304583271344503, 2.4583, 1007.5416666666666, 31.661875128746033, 67.91666666666667, 23.333333333333332, 0.680000014603138, "few clouds,light rain,scattered clouds"),
    ("2025-04-13T00:00:00", "Kasetsart University", 2.7039999553135465, 2.8571, 1007.9142857142857, 32.04371452331543, 75.28571428571429, 33.05714285714286, 3.4099999740719795, "few clouds,light rain,overcast clouds,scattered clouds")
]

MOCK_WEATHER_DATA = [
  ("2025-04-12T17:00:00", "Kasetsart University", 3.09, 3, 1009, 29.07, 77, 20, 0.15, "light rain"),
  ("2025-04-13T00:00:00", "Kasetsart University", 3.09, 3, 1009, 29.07, 77, 20, 0.15, "light rain"),
  ("2025-04-13T00:30:00", "Kasetsart University", 3.6, 4, 1008, 29.84, 75, 20, 0.15, "light rain"),
  ("2025-04-13T01:00:00", "Kasetsart University", 3.09, 3, 1008, 29.07, 82, 20, 0.15, "light rain"),
  ("2025-04-13T01:30:00", "Kasetsart University", 3.6, 4, 1008, 28.94, 82, 20, 0.13, "light rain"),
  ("2025-04-13T02:00:00", "Kasetsart University", 3.09, 3, 1008, 28.94, 83, 20, 0.13, "light rain"),
  ("2025-04-13T02:30:00", "Kasetsart University", 2.57, 3, 1008, 28.82, 83, 20, 0.12, "light rain"),
  ("2025-04-13T03:00:00", "Kasetsart University", 2.57, 3, 1008, 28.82, 83, 20, 0.13, "light rain"),
  ("2025-04-13T03:30:00", "Kasetsart University", 2.06, 2, 1008, 28.04, 87, 20, 0.13, "light rain"),
  ("2025-04-13T04:00:00", "Kasetsart University", 1.54, 2, 1008, 29.81, 91, 20, 0.12, "light rain"),
  ("2025-04-13T04:30:00", "Kasetsart University", 2.06, 2, 1008, 28.04, 87, 20, 0.11, "light rain"),
  ("2025-04-13T05:00:00", "Kasetsart University", 2.57, 3, 1008, 28.04, 87, 20, 0.11, "light rain"),
  ("2025-04-13T05:30:00", "Kasetsart University", 2.06, 2, 1008, 27.92, 87, 20, 0.12, "light rain"),
  ("2025-04-13T06:00:00", "Kasetsart University", 0.51, 1, 1008, 28.51, 91, 20, 0.12, "light rain"),
  ("2025-04-13T06:30:00", "Kasetsart University", 1.54, 2, 1009, 29.68, 93, 20, 0.12, "light rain"),
  ("2025-04-13T07:00:00", "Kasetsart University", 1.54, 2, 1009, 29.24, 88, 20, 0.12, "light rain"),
  ("2025-04-13T07:30:00", "Kasetsart University", 1.03, 1, 1010, 30.87, 87, 20, 0.12, "light rain"),
  ("2025-04-13T08:00:00", "Kasetsart University", 2.06, 2, 1010, 31.02, 81, 20, 0, "few clouds"),
  ("2025-04-13T08:30:00", "Kasetsart University", 2.57, 3, 1010, 31.8, 78, 40, 0, "scattered clouds"),
  ("2025-04-13T09:00:00", "Kasetsart University", 2.06, 2, 1010, 32.4, 77, 40, 0, "scattered clouds"),
  ("2025-04-13T09:30:00", "Kasetsart University", 2.06, 2, 1010, 33.81, 67, 40, 0, "scattered clouds"),
  ("2025-04-13T10:00:00", "Kasetsart University", 2.57, 3, 1010, 33.64, 65, 20, 0, "few clouds"),
  ("2025-04-13T10:30:00", "Kasetsart University", 2.57, 3, 1010, 34.13, 68, 20, 0, "few clouds"),
  ("2025-04-13T11:00:00", "Kasetsart University", 2.57, 3, 1010, 34.8, 66, 40, 0, "scattered clouds"),
  ("2025-04-13T11:30:00", "Kasetsart University", 3.09, 3, 1009, 34.86, 66, 40, 0, "scattered clouds"),
  ("2025-04-13T12:00:00", "Kasetsart University", 2.06, 2, 1009, 35.57, 61, 40, 0, "scattered clouds"),
  ("2025-04-13T12:30:00", "Kasetsart University", 4.73, 5, 1007, 36.2, 63, 31, 0, "scattered clouds"),
  ("2025-04-13T13:00:00", "Kasetsart University", 4.36, 4, 1007, 36.6, 64, 29, 0.13, "light rain"),
  ("2025-04-13T13:30:00", "Kasetsart University", 3.6, 4, 1006, 35.06, 66, 40, 0, "scattered clouds"),
  ("2025-04-13T14:00:00", "Kasetsart University", 3.6, 4, 1006, 35.45, 65, 40, 0, "scattered clouds"),
  ("2025-04-13T14:30:00", "Kasetsart University", 3.09, 3, 1005, 36.32, 53, 40, 0, "scattered clouds"),
  ("2025-04-13T15:00:00", "Kasetsart University", 3.25, 3, 1005, 37.04, 62, 89, 0, "overcast clouds"),
  ("2025-04-13T15:30:00", "Kasetsart University", 2.06, 2, 1005, 36.82, 52, 40, 0, "scattered clouds"),
  ("2025-04-13T16:00:00", "Kasetsart University", 2.06, 2, 1005, 33.93, 60, 40, 0, "scattered clouds"),
  ("2025-04-13T16:30:00", "Kasetsart University", 4.88, 5, 1005, 34.28, 79, 94, 0.6, "light rain"),
  ("2025-04-13T17:00:00", "Kasetsart University", 4.88, 5, 1005, 34.15, 79, 94, 0.65, "light rain")
]


class BaseTestCase(unittest.TestCase):
    """Base helper functions for testcases."""
    def setUp(self) -> None:
        self._url = "http://127.0.0.1:8000/explan/"
        self.client = TestClient(app_api)

    def check_schema(self, schema: Collection[str], data: dict):
        for items in schema:
            self.assertIn(items, data)

    def check_date_diff(self, start_date: str, end_date: str, date_interval: int):
        date1 = self.get_date_object(start_date)
        date2 = self.get_date_object(end_date)
        if date1.day == date2.day:
            self.assertEqual(0, date_interval)
        else:
            date_diff = date1 - date2
            self.assertEqual(abs(date_diff.days), date_interval)

    def get_date_object(self, date_str: str) -> datetime:
        return datetime.fromisoformat(date_str)


class Schemas(Enum):
    weather = ["ts", "location", "wind_speed", "wind_degree", "pressure", "temperature", "humidity", "cloud_percent", "rainfall", "weather"]
    temperature = ["ts", "location", "temperature"]
    humidity = ["ts", "location", "humidity"]
    rainfall = ["ts", "location", "rainfall", "weather"]

    @classmethod
    def get_schema(cls, schema: str) -> list[str]:
        if schema not in cls.__members__:
            raise ValueError('invalid schema referenced')
        return Schemas[schema].value
