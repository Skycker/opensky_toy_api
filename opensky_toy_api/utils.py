from math import sin, cos, radians, atan2, sqrt

EARTH_RADIUS = 6371  # in kilometers


def distance_between_coordinates(latitude1, latitude2, longitude1, longitude2):
    """ Distance between two geographic coordinates
    Algorithm: http://www.movable-type.co.uk/scripts/latlong.html
    Coordinates should be WGS-84 in decimal degrees
    """

    delta_latitude = radians(latitude2 - latitude1)
    delta_longitude = radians(longitude2 - longitude1)

    a = sin(delta_latitude / 2) ** 2 + cos(radians(latitude1)) * cos(radians(latitude2)) * (
        sin(delta_longitude / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(c * EARTH_RADIUS, 1)
