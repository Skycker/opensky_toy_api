import requests
from requests.exceptions import RequestException

from opensky_toy_api.exceptions import OpenSkyApiException
from opensky_toy_api.utils import distance_between_coordinates


class AirplaneState(object):
    """ Abstraction to keep info about plane at some moment """

    def __init__(self, callsign, latitude, longitude):
        self.callsign = callsign
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        if self.callsign:
            return self.callsign
        return super(AirplaneState, self).__str__()

    def get_distance_to(self, latitude, longitude):
        """ Get distance between plane and given coordinates
        :param latitude: WGS-84 latitude in decimal degrees
        :param longitude: WGS-84 longitude in decimal degrees
        :returns [float] distance in kilometers or None if distance can't be calculated
        """

        if not self.latitude or not self.longitude:
            return None
        return distance_between_coordinates(self.latitude, latitude, self.longitude, longitude)


class OpenSkyApi(object):
    """ Interface to user opensky service """

    ROOT_URL = 'https://opensky-network.org/api'
    ALL_STATES_ENDPOINT = '/states/all'

    PARIS_LATITUDE = 48.8588377
    PARIS_LONGITUDE = 2.2770204
    DEFAULT_RADIUS = 450

    PARSE_ERROR = "Can't parse response from opensky"
    REQUEST_ERROR = "Can't get valid response from opensky"

    def parse_response(self, response):
        try:
            return [AirplaneState(state[1], state[6], state[5]) for state in response['states']]
        except (KeyError, IndexError):
            raise OpenSkyApiException(self.PARSE_ERROR)

    def get_states(self):
        """ Get all planes from opensky service 
        :returns [list] List of suitable AirplaneState objects
        :raise OpenSkyApiException if problems with getting or parsing response fro opensky
        """

        try:
            response = requests.get(self.ROOT_URL + self.ALL_STATES_ENDPOINT)
            response = response.json()
        except ValueError:
            raise OpenSkyApiException(self.PARSE_ERROR)
        except RequestException:
            raise OpenSkyApiException(self.REQUEST_ERROR)
        return self.parse_response(response)

    def get_states_near_place(self, latitude=PARIS_LATITUDE, longitude=PARIS_LONGITUDE, radius=DEFAULT_RADIUS):
        """ Get planes not far from given coordinates more than given radius
        :param latitude: WGS-84 latitude in decimal degrees (default Paris latitude)
        :param longitude: WGS-84 longitude in decimal degrees (default Paris longitude)
        :param radius: distance in km (default 450 km)
        :returns [list] List of suitable AirplaneState objects
        :raise OpenSkyApiException if problems with getting or parsing response fro opensky
        """

        states = []
        for state in self.get_states():
            distance = state.get_distance_to(latitude, longitude)
            if distance and distance <= radius:
                states.append(state)
        return states
