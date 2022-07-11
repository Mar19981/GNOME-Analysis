import zipfile, os, sys
import numpy as np
from magnetometer import Signal, Magnetometer


sensors: dict[str, Magnetometer] = {}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments!")
        sys.exit(1)
    
    path = f"./data/{sys.argv[1]}.zip"
    
    magnetometers: list[list[Signal]] = []
    
    with zipfile.ZipFile(path) as zip:
        for name in zip.namelist():
            if zipfile.Path(path, name).is_file():
                magnetometers.append([])
                print(data)
                # with zip.open(name) as file:
                #     for line in file:
                #         time, value = list(map(lambda x: float(x), line.decode().strip().split(" ")))
                #         signal = Signal(time, value)
                #         magnetometers[len(magnetometers) - 1].append(signal)
    print(magnetometers)