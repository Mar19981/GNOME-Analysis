import typing
import math

import scipy.constants as const

import numpy as np


# Earth radius in meters


EARTH_RADIUS = 6.371e6


# Domain wall speed in meters per second


DOMAIN_WALL_SPEED = const.speed_of_light

# WGS-84 Axes


SEMI_MAJOR_AXIS = 6.378137e6


SEMI_MINOR_AXIS = 6.356752314245e6

E = math.sqrt(SEMI_MAJOR_AXIS * SEMI_MAJOR_AXIS -
              SEMI_MINOR_AXIS * SEMI_MINOR_AXIS) / SEMI_MAJOR_AXIS


class Coordinates(typing.NamedTuple):
    lat: float
    lon: float

    h: float
    alt: float
    az: float


class Position(typing.NamedTuple):

    x: float
    y: float
    z: float


class Signal(typing.NamedTuple):

    time: float
    value: float


class Magnetometer:

    def __init__(self, city: str, noise: float, coordinates: Coordinates):

        self.__noise = noise * const.pico

        self.__name = city

        self.__position = np.empty(3)
        self.__llh_to_ecef(coordinates)
        self.__position_norm = self.__position / np.linalg.norm(self.__position)

    def __llh_to_ecef(self, coordinates: Coordinates):

        lat_rad = np.deg2rad(coordinates.lat)
        lon_rad = np.deg2rad(coordinates.lon)

        cosphi = np.cos(lon_rad)
        sinphi = np.sin(lon_rad)
        coslambda = np.cos(lat_rad)
        sinlambda = np.sin(lat_rad)

        n = SEMI_MAJOR_AXIS / math.sqrt(1.0 - E * E * sinphi * sinphi)

        self.__position[0] = (n + coordinates.h) * cosphi * coslambda
        self.__position[1] = (n + coordinates.h) * cosphi * sinlambda
        self.__position[2] = (n * (1.0 - E * E) + coordinates.h) * sinphi

    def __str__(self):
        return f"{self.__name} -  Noise: {self.__noise}pT\n Location: [{self.__position[0]}, {self.__position[1]}, {self.__position[2]}]m\n"

    def __repr__(self):
        info = f"Name: {self.__name} - Noise: {self.__noise} - x: {self.__position[0]} - y: {self.__position[1]} - z: {self.__position[2]}"
        normalized = f"Normalized: x - {self.__position_norm[0]} - y - {self.__position_norm[1]} - z - {self.__position_norm[2]}"
        return f"{info}\n{normalized}\n"
