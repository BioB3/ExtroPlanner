from test_template import BaseTestCase, Schemas
import json


class TestWeather(BaseTestCase):
    def test_get_latest_weather_data(self):
        res = self.client.get(self._url + 'weather?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.check_schema(Schemas.get_schema('weather'), data)

    def test_get_latest_weather_data_with_unknown_location(self):
        res = self.client.get(
            self._url + 'weather?location=123334')
        self.assertEqual(404, res.status_code)

    def test_get_latest_weather_data_with_no_location(self):
        res = self.client.get(
            self._url + 'weather')
        self.assertEqual(422, res.status_code)

    def test_get_weather_data(self):
        res = self.client.get(
            self._url + 'weather?location=Kasetsart%20University&datetime=2025-03-21T22%3A30%3A00')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.check_schema(Schemas.get_schema('weather'), data)

    def test_get_invalid_date_weather_data(self):
        res = self.client.get(
            self._url + 'weather?location=Kasetsart%20University&datetime=12345')
        self.assertEqual(422, res.status_code)
