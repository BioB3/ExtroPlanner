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
            self._url + 'rainfall/max?location=Kasetsart%20University')
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
            self._url + 'rainfall/min?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, dict)
        self.assertEqual(0.0, data['rainfall'])

    def test_get_max_temp_with_unknown_location(self):
        res = self.client.get(
            self._url + 'temperature/max?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_min_temp_with_unknown_location(self):
        res = self.client.get(
            self._url + 'temperature/min?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_max_temp_with_no_location(self):
        res = self.client.get(
            self._url + 'temperature/max')
        self.assertEqual(422, res.status_code)

    def test_get_min_temp_with_no_location(self):
        res = self.client.get(
            self._url + 'temperature/min')
        self.assertEqual(422, res.status_code)

    def test_get_max_temp_with_invalid_date(self):
        res = self.client.get(
            self._url + 'temperature/max?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)

    def test_min_temp_with_invalid_date(self):
        res = self.client.get(
            self._url + 'temperature/min?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)

    def test_get_max_humidity_with_unknown_location(self):
        res = self.client.get(
            self._url + 'humidity/max?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_min_humidity_with_unknown_location(self):
        res = self.client.get(
            self._url + 'humidity/min?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_max_humidity_with_no_location(self):
        res = self.client.get(
            self._url + 'humidity/max')
        self.assertEqual(422, res.status_code)

    def test_get_min_humidity_with_no_location(self):
        res = self.client.get(
            self._url + 'humidity/min')
        self.assertEqual(422, res.status_code)

    def test_get_max_humidity_with_invalid_date(self):
        res = self.client.get(
            self._url + 'humidity/max?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)

    def test_min_humidity_with_invalid_date(self):
        res = self.client.get(
            self._url + 'humidity/min?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)

    def test_get_max_rainfall_with_unknown_location(self):
        res = self.client.get(
            self._url + 'rainfall/max?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_min_rainfall_with_unknown_location(self):
        res = self.client.get(
            self._url + 'rainfall/min?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_max_rainfall_with_no_location(self):
        res = self.client.get(
            self._url + 'rainfall/max')
        self.assertEqual(422, res.status_code)

    def test_get_min_rainfall_with_no_location(self):
        res = self.client.get(
            self._url + 'rainfall/min')
        self.assertEqual(422, res.status_code)

    def test_get_max_rainfall_with_invalid_date(self):
        res = self.client.get(
            self._url + 'rainfall/max?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)

    def test_min_rainfall_with_invalid_date(self):
        res = self.client.get(
            self._url + 'rainfall/min?location=Kasetsart%20University&days=0')
        self.assertEqual(422, res.status_code)
