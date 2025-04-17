from test_template import BaseTestCase, MOCK_WEATHER_DATA
import json
from unittest import mock


class TestMinMaxWeather(BaseTestCase):
    @mock.patch('api.app.pool')
    def test_get_max_temperature(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = max(MOCK_WEATHER_DATA, key=lambda x: x[5])
        mock_cursor.fetchone.return_value = (max_data[0], max_data[1], max_data[5])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'temperature/max?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(37.04, data['temperature'])

    @mock.patch('api.app.pool')
    def test_get_min_temperature(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = min(MOCK_WEATHER_DATA, key=lambda x: x[5])
        mock_cursor.fetchone.return_value = (
        max_data[0], max_data[1], max_data[5])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'temperature/min?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(27.92, data['temperature'])

    @mock.patch('api.app.pool')
    def test_get_max_humidity(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = max(MOCK_WEATHER_DATA, key=lambda x: x[6])
        mock_cursor.fetchone.return_value = (
        max_data[0], max_data[1], max_data[6])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'humidity/max?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(93.0, data['humidity'])

    @mock.patch('api.app.pool')
    def test_get_min_humidity(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = min(MOCK_WEATHER_DATA, key=lambda x: x[6])
        mock_cursor.fetchone.return_value = (
            max_data[0], max_data[1], max_data[6])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'humidity/min?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(52.0, data['humidity'])

    @mock.patch('api.app.pool')
    def test_get_max_rainfall(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = max(MOCK_WEATHER_DATA, key=lambda x: x[8])
        mock_cursor.fetchone.return_value = (
        max_data[0], max_data[1], max_data[8], max_data[9])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'rain/max?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(0.65, data['rainfall'])

    @mock.patch('api.app.pool')
    def test_get_min_rainfall(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        max_data = min(MOCK_WEATHER_DATA, key=lambda x: x[8])
        mock_cursor.fetchone.return_value = (
            max_data[0], max_data[1], max_data[8], max_data[9])
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'rain/min?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(0.0, data['rainfall'])
