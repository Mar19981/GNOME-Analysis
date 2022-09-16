import typing
import math

import scipy.constants as const

import numpy as np


# Earth radius in meters


EARTH_RADIUS = 6.371e6


# Domain wall speed in meters per second


DOMAIN_WALL_SPEED = const.speed_of_light

# Tangential speed on the Equator in meters per second

EQUATOR_TANGENTIAL_SPEED = 465.11

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

    def __init__(self, city: str, coordinates: Coordinates):

        self.__name = city
        self.__signals = None
        self.__filtered_signal = None
        self.__timestamps = None
        self.__filtered_timestamps = None
        self.__noise = None
        self.__cov = None
        self.__samples = 0
        self.__filtered_samples = 0
        self.__frequency = 0.0

        self.__az = coordinates.az
        self.__alt = coordinates.alt
        self.__position = np.empty(3)
        self.__time_shift = 0.0
        self.__llh_to_ecef(coordinates)
        self.__position_norm = self.__position / \
            np.linalg.norm(self.__position)

    def __llh_to_ecef(self, coordinates: Coordinates):

        lat_rad = np.deg2rad(coordinates.lat)
        lon_rad = np.deg2rad(coordinates.lon)

        cosphi = np.cos(lon_rad)
        sinphi = np.sin(lon_rad)
        self.__coslambda = np.cos(lat_rad)
        sinlambda = np.sin(lat_rad)

        n = SEMI_MAJOR_AXIS / math.sqrt(1.0 - E * E * sinphi * sinphi)

        self.__position[0] = (n + coordinates.h) * cosphi * self.__coslambda
        self.__position[1] = (n + coordinates.h) * cosphi * sinlambda
        self.__position[2] = (n * (1.0 - E * E) + coordinates.h) * sinphi

    @property
    def name(self) -> str:
        return self.__name

    @property
    def position_normalized(self):
        return self.__position_norm

    @property
    def noise(self) -> float:
        return self.__noise

    @property
    def alt(self) -> float:
        return self.__alt

    @property
    def az(self) -> float:
        return self.__az

    @property
    def signals(self):
        return self.__signals

    @property
    def filtered_signal(self):
        return self.__filtered_signal

    @property
    def filtered_samples(self) -> int:
        return self.__filtered_samples

    @property
    def timestamps(self):
        return self.__timestamps

    @property
    def filtered_timestamps(self):
        return self.__filtered_timestamps

    @property
    def cov(self) -> float:
        return self.__cov

    @property
    def x_norm(self):
        return self.__position_norm[0]

    @property
    def y_norm(self):
        return self.__position_norm[1]

    @property
    def z_norm(self):
        return self.__position_norm[2]

    def __str__(self):
        return f"{self.__name} -  Noise: {self.__noise}\nLocation: [{self.__position[0]}, {self.__position[1]}, {self.__position[2]}]m\nSamples - {self.__samples} Frequency - {self.__frequency}\n"

    def __repr__(self):
        info = f"Name: {self.__name} - Noise: {self.__noise} - x: {self.__position[0]} - y: {self.__position[1]} - z: {self.__position[2]}"
        normalized = f"Normalized: x - {self.__position_norm[0]} - y - {self.__position_norm[1]} - z - {self.__position_norm[2]}"
        return f"{info}\n{normalized}\n{self.__timestamps}\n {self.__signals}\nSamples - {self.__samples} Frequency - {self.__frequency}\n"

    def calculate_time_shift(self, reference):
        tangential_speed = self.__coslambda * EQUATOR_TANGENTIAL_SPEED

    def add_signals(self, timestamps, signals):
        self.__timestamps = np.array(timestamps)
        self.__signals = np.array(signals)
        self.__noise = np.std(self.__signals)
        self.__cov = 1.0 / self.__noise
        self.__samples = len(timestamps)
        self.__frequency = self.__samples / \
            (timestamps[self.__samples - 1] - timestamps[0])
        self.__filtered_signal = np.zeros_like(self.__signals)
        self.__filter_signals()

    def get_signal_peak(self):
        if (self.__signals is not None):
            index: int = np.argmax(np.absolute(self.__filtered_signal))
            return Signal(self.__filtered_timestamps[index], self.__filtered_signal[index])

    def get_signal_peak_index(self, start: int = 0, end: int = None):
        if end is None:
            end = self.__samples
        if (self.__signals is not None):
            index: int = np.argmax(np.absolute(
                self.__signals[start:end]))
            return start + index

    def get_filtered_signal_peak_index(self, start: int = 0, end: int = None):
        if end is None:
            end = self.__samples
        if (self.__signals is not None):
            index: int = np.argmax(np.absolute(
                self.__filtered_signal[start:end]))
            return start + index

    def __filter_signals(self):

        filtered_response = self.__noise * 3.0 < np.absolute(self.__signals)

        self.__filtered_signal[filtered_response] = self.__signals[filtered_response]
        self.__filtered_signal = np.convolve(
            self.__filtered_signal, np.ones(16), "valid") * 0.0625
        self.__filtered_timestamps = np.linspace(
            self.__timestamps[0], self.__timestamps[-1], len(self.__filtered_signal))
        self.__filtered_samples = len(self.__filtered_signal)
