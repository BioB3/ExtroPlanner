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


class BaseTestCase(unittest.TestCase):
    """Base helper functions for testcases."""
    def setUp(self) -> None:
        self._url = "http://127.0.0.1:8000/explan/"
        self.client = TestClient(app_api)

    def check_schema(self, schema: Collection[str], data: dict):
        for items in schema:
            self.assertIn(items, data)

    def check_date_diff(self, date1: str, date2: str, date_interval: int):
        date_diff = self.get_date_object(date1) - self.get_date_object(date2)
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
