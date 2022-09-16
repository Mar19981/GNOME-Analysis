import zipfile
import re
import numpy as np
import magnetometer as mg
import graphs as gr


class Network:
    def __init__(self):
        self.__magnetometers = {}
        self.__reference_magnetometer = ""
        self.__domain_wall_vector = np.empty(3)

    @property
    def reference_magnetometer(self) -> str:
        return self.__reference_magnetometer

    @reference_magnetometer.setter
    def reference_magnetometer(self, reference: str):
        self.__reference_magnetometer = reference

    def add_magnetometer(self, location: str, sensor: mg.Magnetometer):
        self.__magnetometers[location] = sensor

    def load_data_from_zip(self, path: str):
        # extracts city name from file name
        expr = re.compile(r"(.*/)([a-z]+)([0-9]{2}\.txt)")
        with zipfile.ZipFile(path) as file:
            for name in file.namelist():
                if zipfile.Path(path, name).is_file() and (res := expr.match(name)) is not None and (res := res.group(2).capitalize()) in self.__magnetometers:
                    with file.open(name) as f:
                        timestamps = []
                        signals = []
                        for line in f:
                            time, value = list(
                                map(lambda x: float(x), line.decode().strip().split(" ")))
                            timestamps.append(time)
                            signals.append(value)
                        self.__magnetometers[res].add_signals(
                            timestamps, signals)

    def __minimize_chi2(self, indices, filtered=True):
        a = np.zeros((3, 3))
        b = np.zeros(3)

        for index, (_, magnetometer) in zip(indices, self.__magnetometers.items()):

            a_xx = magnetometer.cov * magnetometer.x_norm * magnetometer.x_norm
            a_xy = magnetometer.cov * magnetometer.x_norm * magnetometer.y_norm
            a_xz = magnetometer.cov * magnetometer.x_norm * magnetometer.z_norm
            a_yy = magnetometer.cov * magnetometer.y_norm * magnetometer.y_norm
            a_yz = magnetometer.cov * magnetometer.y_norm * magnetometer.z_norm
            a_zz = magnetometer.cov * magnetometer.z_norm * magnetometer.z_norm

            a[0, 0] += a_xx
            a[0, 1] += a_xy
            a[0, 2] += a_xz

            a[1, 0] += a_xy
            a[1, 1] += a_yy
            a[1, 2] += a_yz

            a[2, 0] += a_xz
            a[2, 1] += a_yz
            a[2, 2] += a_zz

            signal = magnetometer.filtered_signal[index] if filtered else magnetometer.signals[index]

            b[0] += magnetometer.cov * magnetometer.x_norm * signal
            b[1] += magnetometer.cov * magnetometer.y_norm * signal
            b[2] += magnetometer.cov * magnetometer.z_norm * signal

        a *= 2.0
        b *= 2.0

        return np.linalg.solve(a, b)

    def plot_raw_signals(self):
        gr.Graphs.plot_data(self.__magnetometers, "Raw signals", "Time", "Signal",
                            lambda ax, sensor: ax.plot(sensor.timestamps, sensor.signals, "--o",
                                                       label=sensor.name, color=np.random.rand(3,)))

    def plot_preprocessed_signals(self):
        gr.Graphs.plot_data(self.__magnetometers, "Filtered signals", "Time", "Signal",
                            lambda ax, sensor: ax.plot(sensor.filtered_timestamps, sensor.filtered_signal, "--o",
                                                       label=sensor.name, color=np.random.rand(3,)))

    def plot_hemisphere(self, filtered: bool = True):
        x_coords = []
        y_coords = []
        z_coords = []
        magnitudes = []
        samples = list(self.__magnetometers.values())[0].filtered_samples
        for i in range(samples):
            indices = np.full(len(self.__magnetometers), i)
            wall = self.__minimize_chi2(indices, filtered)
            magnitudes.append(np.linalg.norm(wall))
            x, y, z = wall
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)

        magnitudes = np.array(magnitudes)
        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        z_coords = np.array(z_coords)
        theta = np.arctan2(x_coords, y_coords)
        magnitudes[magnitudes == 0] = 1.0
        r = np.arccos(z_coords / magnitudes)

        gr.Graphs.plot_hemisphere(
            theta, r, magnitudes, f"Chi-squared magnitudes ({'Filtered' if filtered else 'Raw'})")

    def find_domain_wall(self):
        indicies = [magnetometer.get_filtered_signal_peak_index()
                    for (_, magnetometer) in self.__magnetometers.items()]
        self.__domain_wall_vector = self.__minimize_chi2(indicies)
        magnitude = np.linalg.norm(self.__domain_wall_vector)
        print(f"Domain wall vector: {self.__domain_wall_vector}")
        print(f"Magnitude: {magnitude}")
        normalized_vector = self.__domain_wall_vector / magnitude
        print("Angles between magnetometers and domain wall:")
        for _, magnetometer in self.__magnetometers.items():
            dot_product = np.dot(
                normalized_vector, magnetometer.position_normalized)
            angle = np.around(np.rad2deg(np.arccos(dot_product)), 3)
            print(f"{magnetometer.name}: {angle}deg")
