import unittest
from unittest.mock import Mock, patch

from requests.exceptions import ConnectionError, Timeout

from opensky_toy_api import AirplaneState, OpenSkyApi, OpenSkyApiException


class TestAirplaneState(unittest.TestCase):
    def test_getting_distance_valid(self):
        first_point = (54.7800533, 31.8598796)
        second_point = (55.7494733, 37.3523218)
        state = AirplaneState(callsign='test plane', latitude=first_point[0], longitude=first_point[1])
        self.assertEqual(state.get_distance_to(*second_point), 364.2)

    def test_getting_distance_empty(self):
        test_point = (1, 2)
        state_without_latitude = AirplaneState(callsign='test plane', latitude=None, longitude=3)
        state_without_longitude = AirplaneState(callsign='another test plane', latitude=4, longitude=None)
        self.assertIs(state_without_latitude.get_distance_to(*test_point), None)
        self.assertIs(state_without_longitude.get_distance_to(*test_point), None)


class TestOpenskyApi(unittest.TestCase):
    def test_getting_planes_errors(self):
        api = OpenSkyApi()
        error_mocks = [Mock(side_effect=ConnectionError), Mock(side_effect=Timeout)]

        for mock in error_mocks:
            with patch('requests.get', mock):
                with self.assertRaises(OpenSkyApiException):
                    api.get_states()

    def test_getting_planes_near(self):
        test_point = (54.7800533, 31.8598796)
        test_radius = 50
        plain_near = AirplaneState('test', 54.8566007, 32.014617)
        plain_far_away = AirplaneState('test', -27.3818631, 152.7130084)

        mock = Mock(return_value=[plain_near, plain_far_away])
        with patch('opensky_toy_api.OpenSkyApi.get_states', mock):
            api = OpenSkyApi()
            states_near = api.get_states_near_place(*test_point, test_radius)
            self.assertIn(plain_near, states_near)
            self.assertNotIn(plain_far_away, states_near)
