import matplotlib.pyplot as plt
import numpy as np
import math


class Graphs:

    @staticmethod
    def plot_data(sensors: dict, title: str, x_label: str, y_label: str, action):
        plt.style.use('seaborn')

        cols = math.ceil(len(sensors) * 0.2)
        fig = plt.figure(figsize=(11, 7), constrained_layout=True)
        spec = fig.add_gridspec(5, cols)
        col = 0
        for index, (_, sensor) in enumerate(sensors.items()):
            row = index % 5
            ax = fig.add_subplot(spec[row, col])
            action(ax, sensor)
            ax.set_ylabel(y_label)
            ax.set_xscale("log")
            ax.legend()

            ax.tick_params(
                axis='x',
                which='both',
                bottom=False,
                top=False,
                labelbottom=False)
            if row == 4 or index == len(sensors) - 1:
                ax.set_xlabel(x_label)
                col += 1

        fig.suptitle(title)
        fig.show()

    @staticmethod
    def plot_hemisphere(az, alt, z, title: str):

        theta = np.linspace(0, 2*np.pi, 50)
        r = np.linspace(0, np.pi * 0.5, 50)
        # making up some data
        theta, r = np.meshgrid(theta, r)

        x_indeces = np.interp(az + np.pi, [0, 2*np.pi], [0, 49]).astype(int)
        y_indeces = np.interp(alt, [0, np.pi], [0, 49]).astype(int)
        values = np.zeros_like(theta)
        for x, y, value in zip(x_indeces, y_indeces, z):
            values[x, y] = value
        fig = plt.figure()
        ax = fig.add_subplot(polar=True)
        cax = ax.contourf(theta, r, values, 100)
        fig.colorbar(cax, ax=ax, pad=0.1)
        fig.suptitle(title)
        fig.show()
