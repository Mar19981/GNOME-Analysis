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

E


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

    def __init__(self, city: str, noise: float, coordinates: Coordinates):

        self.__noise = noise * const.pico

        self.__name = city

        self.__LLH2ECEF(coordinates)
        

    def __LLH2ECEF(self, coordinates: Coordinates):
        
        latRad = np.deg2rad(coordinates.lat)

        lonRad = np.deg2rad(coordinates.lon)


        cosphi = np.cos(lonRad)

        sinphi = np.sin(lonRad)


        coslambda = np.cos(latRad)


        sinlambda = np.sin(latRad)


        n = SEMI_MAJOR_AXIS / math.sqrt(1.0 - E * E * sinphi * sinphi)
        


        self.__x = (n + coordinates.h) * cosphi * coslambda


        self.__y = (n + coordinates.h) * cosphi * sinlambda


        self.__z = (n * (1.0 - E * E) + coordinates.h) * sinphi
        
    def __str__(self):


        return f"{self.__name} -  Noise: {self.__noise}pT Location: [{self.__x}, {self.__y}, {self.__z}]m"
    def __repr__(self):


        return f"Name: {self.__name} - Noise: {self.__noise} - x: {self.__x} - y: {self.__y} - z: {self.__z}"
    
        
    


