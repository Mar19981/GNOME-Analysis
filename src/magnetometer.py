from typing import NamedTuple
import scipy.constants as const
import numpy as np
import math

#Earth radius in meters
EARTH_RADIUS = 6.371e6
#Domain wall speed in meters per second
DOMAIN_WALL_SPEED = const.speed_of_light

#1 degree in radians
DEGREE_RAD = const.pi / 180.0

#WGS-84 Axes
SEMI_MAJOR_AXIS = 6.378137e6
SEMI_MINOR_AXIS = 6.356752314245e6


class Coordinates(NamedTuple):
    lat: float
    lon: float
    h: float
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
    def __LLH2EGEC(self, coordinates:Coordinates):
        latRad = np.deg2rad(coordinates.lat)
        lonRad = np.deg2rad(coordinates.lon)
        e = math.sqrt(SEMI_MAJOR_AXIS * SEMI_MAJOR_AXIS - SEMI_MINOR_AXIS * SEMI_MINOR_AXIS) / SEMI_MAJOR_AXIS
        cosphi = np.cos(lonRad)
        sinphi = np.sin(lonRad)
        coslambda = np.cos(latRad)
        sinlambda = np.sin(latRad)
        n = SEMI_MAJOR_AXIS / math.sqrt(1 - e * e * sinphi * sinphi)
        
        self.__x = (n + coordinates.h) * cosphi * coslambda
        self.__y = (n + coordinates.h) * cosphi * sinlambda
        self.__z = (n * (1 - e * e) + coordinates.h) * sinphi
        
    
