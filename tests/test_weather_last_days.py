from test_template import BaseTestCase, Schemas, MOCK_WEATHER_DATA
import json
from unittest import mock


class TestLastWeather(BaseTestCase):
    @mock.patch('api.app.pool')
    def test_get_default_last_weather_data(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = MOCK_WEATHER_DATA[1::]
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'weather/last?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.check_date_diff(data[1]['ts'], data[0]['ts'], 0)
        for items in data:
            self.check_schema(Schemas.get_schema('weather'), items)

    def test_get_last_weather_data_with_invalid_location(self):
        res = self.client.get(
            self._url + 'weather/last?location=123334')
        self.assertEqual(404, res.status_code)

    def test_get_last_weather_data_with_no_location(self):
        res = self.client.get(
            self._url + 'weather/last')
        self.assertEqual(422, res.status_code)

    @mock.patch('api.app.pool')
    def test_get_weather_data_from_last_2_days(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = MOCK_WEATHER_DATA
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'weather/last?location=Kasetsart%20University&days=7')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.check_date_diff(data[-1]['ts'], data[0]['ts'], 1)
        for items in data:
            self.check_schema(Schemas.get_schema('weather'), items)

    def test_get_last_weather_data_with_invalid_days(self):
        res = self.client.get(
            self._url + 'weather/last?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)
