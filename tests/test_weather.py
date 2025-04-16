from test_template import BaseTestCase, Schemas
import requests
import json


class TestWeather(BaseTestCase):
    def test_get_latest_weather_data(self):
        res = requests.get(self._url + 'weather?location=Kasetsart%20University')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.check_schema(Schemas.get_schema('weather'), data)

    def test_get_latest_weather_data_with_invalid_location(self):
        res = requests.get(
            self._url + 'weather?location=123334')
        self.assertEqual(res.status_code, 404)

    def test_get_latest_weather_data_with_no_location(self):
        res = requests.get(
            self._url + 'weather')
        self.assertEqual(res.status_code, 400)

    def test_get_weather_data(self):
        # TODO: Add date check
        res = requests.get(
            self._url + 'weather?location=Kasetsart%20University')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.check_schema(Schemas.get_schema('weather'), data)

    def test_get_invalid_date_weather_data(self):
        pass
