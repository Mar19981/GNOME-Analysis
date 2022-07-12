from typing import NamedTuple

import scipy.constants as const

import numpy as np

import math



#Earth radius in meters


EARTH_RADIUS = 6.371e6


#Domain wall speed in meters per second


DOMAIN_WALL_SPEED = const.speed_of_light



#WGS-84 Axes


SEMI_MAJOR_AXIS = 6.378137e6


SEMI_MINOR_AXIS = 6.356752314245e6

E = math.sqrt(SEMI_MAJOR_AXIS * SEMI_MAJOR_AXIS - SEMI_MINOR_AXIS * SEMI_MINOR_AXIS) / SEMI_MAJOR_AXIS


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

        self.__position = np.empty(3)
        
        self.__LLH2ECEF(coordinates)
        

    def __LLH2ECEF(self, coordinates: Coordinates):
        
        latRad = np.deg2rad(coordinates.lat)

        lonRad = np.deg2rad(coordinates.lon)


        cosphi = np.cos(lonRad)

        sinphi = np.sin(lonRad)


        coslambda = np.cos(latRad)


        sinlambda = np.sin(latRad)


        n = SEMI_MAJOR_AXIS / math.sqrt(1.0 - E * E * sinphi * sinphi)
        


        self.__position[0] = (n + coordinates.h) * cosphi * coslambda


        self.__position[1] = (n + coordinates.h) * cosphi * sinlambda


        self.__position[2] = (n * (1.0 - E * E) + coordinates.h) * sinphi
        
    def __str__(self):
        return f"{self.__name} -  Noise: {self.__noise}pT Location: [{self.__position[0]}, {self.__position[1]}, {self.__position[2]}]m"
    
    def __repr__(self):
        return f"Name: {self.__name} - Noise: {self.__noise} - x: {self.__position[0]} - y: {self.__position[1]} - z: {self.__position[2]}"
    
        
    


