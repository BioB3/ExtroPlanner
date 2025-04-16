import unittest
from enum import Enum
from collections.abc import Collection


class BaseTestCase(unittest.TestCase):
    """Base helper functions for testcases."""
    def setUp(self) -> None:
        self._url = "http://127.0.0.1:8000/explan/"

    def check_schema(self, schema: Collection[str], data: dict):
        for items in schema:
            self.assertIn(items, data)

    def check_date_diff(self):
        pass


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
