import argparse

import matplotlib.pyplot as plt

import network as n
from magnetometer import Magnetometer, Coordinates


sensors: dict[str, Magnetometer] = {
    "Krakow": Magnetometer("Krakow", Coordinates(50.0289, 19.9048, 219.0, 45.0, 0.0)),
    "Beijing": Magnetometer("Beijing", Coordinates(40.2457, 116.1868, 44.0, 251.0, 0.0)),
    "Berkeley": Magnetometer("Berkeley", Coordinates(37.8723, -122.2570, 52.0, 0.0, 90.0)),
    "Daejeon": Magnetometer("Daejeon", Coordinates(36.3909, 127.3987, 72.0, 0.0, 90.0)),
    "Fribourg": Magnetometer("Fribourg", Coordinates(37.6564, 7.1581, 610.0, 190.0, 0.0)),
    "Hayward": Magnetometer("Hayward", Coordinates(46.7930, -122.0539, 34.0, 0.0, -90.0)),
    "Hefei": Magnetometer("Hefei", Coordinates(31.8429, 117.2526, 37.0, 90.0, 0.0)),
    "Lewisburg": Magnetometer("Lewisburg", Coordinates(40.9557, -76.8825, 634.0, 0.0, 90.0)),
    "Mainz": Magnetometer("Mainz", Coordinates(49.9915, 8.2354, 89.0, 0.0, -90.0))

}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input", help="Zip file name contained in data directory")
    parser.add_argument("--plot_signal_raw", "--pr",
                        help="Plot raw signal data", action="store_true")
    parser.add_argument("--plot_signal_filtered", "--pf",
                        help="Plot filtered signal data", action="store_true")
    parser.add_argument("--plot_hemisphere_raw", "--phr",
                        help="Plot chi squares data on hemisphere from raw signal", action="store_true")
    parser.add_argument("--plot_hemisphere_filtered", "--phf",
                        help="Plot chi squares data on hemisphere from filtered signal", action="store_true")

    arguments = parser.parse_args()

    path = f"./data/{arguments.input}.zip"
    network = n.Network()
    for location, sensor in sensors.items():
        network.add_magnetometer(location, sensor)

    network.load_data_from_zip(path)
    network.find_domain_wall()

    if arguments.plot_signal_raw:
        network.plot_raw_signals()

    if arguments.plot_signal_filtered:
        network.plot_preprocessed_signals()

    if arguments.plot_hemisphere_raw:
        network.plot_hemisphere(False)

    if arguments.plot_hemisphere_filtered:
        network.plot_hemisphere(True)

    plt.show()


if __name__ == "__main__":
    main()
