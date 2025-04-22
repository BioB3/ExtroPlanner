from test_template import BaseTestCase, Schemas, MOCK_AGGREGATE_DATA
import json
from unittest import mock


class TestAggregateWeather(BaseTestCase):
    @mock.patch('api.app.pool')
    def test_get_default_weather_aggregation(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [MOCK_AGGREGATE_DATA[0]]
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'weather/aggregate?location=Kasetsart%20University')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        for items in data:
            self.check_schema(Schemas.get_schema('weather'), items)

    def test_get_aggregate_weather_data_with_unknown_location(self):
        res = self.client.get(
            self._url + 'weather/aggregate?location=12345')
        self.assertEqual(404, res.status_code)

    def test_get_aggregate_weather_data_with_no_location(self):
        res = self.client.get(
            self._url + 'weather/aggregate')
        self.assertEqual(422, res.status_code)

    @mock.patch('api.app.pool')
    def test_get_weather_aggregation_from_last_7_days(self, mock_pool_db):
        mock_conn = mock.MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = MOCK_AGGREGATE_DATA
        mock_pool_db.connection.return_value.__enter__.return_value = mock_conn
        res = self.client.get(
            self._url + 'weather/aggregate?location=Kasetsart%20University&days=7')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.text)
        self.assertIsInstance(data, list)
        self.assertEqual(7, len(data))
        self.assertIsInstance(data[0], dict)
        self.check_date_diff(data[1]['ts'], data[0]['ts'], 1)
        for items in data:
            self.check_schema(Schemas.get_schema('weather'), items)

    def test_get_aggregate_weather_data_with_invalid_days(self):
        res = self.client.get(
            self._url + 'weather/aggregate?location=Kasetsart%20University&days=-1')
        self.assertEqual(422, res.status_code)
