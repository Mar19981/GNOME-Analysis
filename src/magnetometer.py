from typing import NamedTuple
import scipy.constants as const

#Earth radius in meters
EARTH_RADIUS = 6.371e6
#Domain wall speed in meters per second
DOMAIN_WALL_SPEED = const.speed_of_light

#1 degree in radians
DEGREE_RAD = const.pi / 180.0



class Coordinates(NamedTuple):
    lat: float
    lon: float
    alt: float
    az: float

class Position(NamedTuple):
    x: float
    y: float
    z: float
    

class Signal(NamedTuple):
    time: float
    value: float

class Magnetometer:
    def __init__(self, noise: float, coordinates: Coordinates):
        pass
    
