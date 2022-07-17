import zipfile
import sys
from magnetometer import Signal, Magnetometer, Coordinates


sensors: dict[str, Magnetometer] = {
    "Krakow": Magnetometer("Krakow", 15.6, Coordinates(50.0289, 19.9048, 219.0, 45.0, 0.0)),
    "Beijing": Magnetometer("Beijing", 10.4, Coordinates(40.2457, 116.1868, 44.0, 251.0, 0.0)),
    "Berkeley": Magnetometer("Berkeley", 14.5, Coordinates(37.8723, -122.2570, 52.0, 0.0, 90.0)),
    "Daejeon": Magnetometer("Daejeon", 116.0, Coordinates(36.3909, 127.3987, 72.0, 0.0, 90.0)),
    "Fribourg": Magnetometer("Fribourg", 12.6, Coordinates(37.6564, 7.1581, 610.0, 190.0, 0.0)),
    "Hayward": Magnetometer("Hayward", 14.3, Coordinates(46.7930, -122.0539, 34.0, 0.0, -90.0)),
    "Hefei": Magnetometer("Hefei", 12.0, Coordinates(31.8429, 117.2526, 37.0, 90.0, 0.0)),
    "Lewisburg": Magnetometer("Lewisburg", 54.5, Coordinates(40.9557, -76.8825, 634.0, 0.0, 90.0)),
    "Mainz": Magnetometer("Mainz", 6.8, Coordinates(49.9915, 8.2354, 89.0, 0.0, -90.0))

}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments!")
        sys.exit(1)

    path = f"./data/{sys.argv[1]}.zip"

    print(sensors)

    magnetometers: list[list[Signal]] = []

    with zipfile.ZipFile(path) as file:
        for name in file.namelist():
            if zipfile.Path(path, name).is_file():
                magnetometers.append([])
                with file.open(name) as file:
                    for line in file:
                        time, value = list(
                            map(lambda x: float(x), line.decode().strip().split(" ")))
                        signal = Signal(time, value)
                        magnetometers[len(magnetometers) - 1].append(signal)
