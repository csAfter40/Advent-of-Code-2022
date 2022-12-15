from typing import List, Tuple, Any, Set
import re
from helpers import print_matrix

class Map(list):
    def __init__(self, offset=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def __getitem__(self, index):
        return super().__getitem__(index-self.offset)
    
    def __setitem__(self, index, value):
        return super().__setitem__(index-self.offset, value)

class App():
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path
        self.data:List[Tuple[Tuple[int]]] = []
        self.map:Map = None
        self.limits:Tuple[int] = None
        self.total_coverage:List[Tuple[int]] = []
        self.sensors:List[Tuple[Any]] = [] 
        self.beacons:Set[Tuple[int]] = set()

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def extract_data(self, line:str) -> Tuple[Tuple]:
        """
        Reads line and returns sensor and beacon coordinates:
        """
        items = re.split(" |=|: |, ", line)
        sensor = (int(items[5]), int(items[3]))
        beacon = (int(items[13]), int(items[11]))
        return sensor, beacon

    def setup_data(self) -> None:
        """
        Reads input and setup data.
        """
        for line in self.get_lines():
            sensor, beacon = self.extract_data(line)
            self.data.append((sensor, beacon))
    
    def get_manhattan_distance(self, item1:Tuple[int], item2:Tuple[int]) -> int:
        """
        Given two coordinates, return Manhattan distance between coordinates.
        """ 
        y_dist = abs(item1[0]-item2[0])
        x_dist = abs(item1[1]-item2[1])
        return y_dist + x_dist

    def set_sensor_data(self) -> None:
        """
        Reads data and creates list of sensors with coverage ranges. 
        """
        for couple in self.data:
            distance = self.get_manhattan_distance(*couple)
            self.sensors.append((couple[0], distance))

    def set_beacon_data(self) -> None:
        """
        Reads data and sets a set of beacons.
        """
        for couple in self.data:
            self.beacons.add(couple[1])

    def get_intersection_points(self, row:int) -> Set[Tuple[int]]:
        """
        Calculates the intersecting points of each sensor's coverage on the 
        given row, removes the baecon points and returns a set of intersection 
        points.
        """
        intersection_points = set()
        for data in self.sensors:
            sensor, length = data
            if sensor[0]-length <= row <= sensor[0]+length:
                intersection = length - abs(sensor[0]-row)
                for i in range(sensor[1]-intersection, sensor[1]+intersection+1):
                    intersection_points.add((row, i))

        for point in self.beacons:
            if point in intersection_points:
                intersection_points.remove(point)
        return intersection_points

if  __name__ == "__main__":
    # row, file_path = 10, "15/test_input.txt"
    row, file_path = 2000000, "15/beacon.txt"
    app = App(file_path)
    app.setup_data()
    app.set_sensor_data()
    app.set_beacon_data()
    points = app.get_intersection_points(row)
    print(len(points))
