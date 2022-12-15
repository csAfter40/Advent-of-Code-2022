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

    def sort_sensor_data(self) -> None:
        """
        Sorts sensor data due to sensor range from min to max.
        """
        self.sensors.sort(key=lambda x: x[1])

    def is_out_of_coverage(self, point:Tuple[int], index:int) -> bool:
        """
        Returns true if point is out of sensor coverage. 
        """
        for i, data in enumerate(self.sensors):
            if i == index:
                continue
            sensor, length = data
            if self.get_manhattan_distance(point, sensor) <= length:
                return False
        return True

    def find_beacon(self, limit:int) -> Tuple[int]: 
        """
        Search points through outer edge of sensor coverage areas and returns 
        first point out of coverage of all sensors.
        """
        for index, data in enumerate(self.sensors[:-1]):
            print(index, data)
            sensor, length = data
            corners = [
                (sensor[0], sensor[1]-length-1),
                (sensor[0]-length-1, sensor[1]),
                (sensor[0], sensor[1]+length+1),
                (sensor[0]+length+1, sensor[1]),
            ] # left, top, right, bottom
            current = corners[0]
            for i in range(length+1):
                point = (current[0]-i,current[1]+i)
                if 0 <= point[0] <= limit and 0 <= point[1] <= limit:
                    if self.is_out_of_coverage(point, index):
                        return point
            current = corners[1]
            for i in range(length+1):
                point = (current[0]+i,current[1]+i)
                if 0 <= point[0] <= limit and 0 <= point[1] <= limit:
                    if self.is_out_of_coverage(point, index):
                        return point
            current = corners[2]
            for i in range(length+1):
                point = (current[0]+i,current[1]-i)
                if 0 <= point[0] <= limit and 0 <= point[1] <= limit:
                    if self.is_out_of_coverage(point, index):
                        return point
            current = corners[3]
            for i in range(length+1):
                point = (current[0]-i,current[1]-i)
                if 0 <= point[0] <= limit and 0 <= point[1] <= limit:
                    if self.is_out_of_coverage(point, index):
                        return point

if  __name__ == "__main__":
    # row, file_path, limit = 10, "15/test_input.txt", 20
    row, file_path, limit = 2000000, "15/beacon.txt", 4000000
    app = App(file_path)
    app.setup_data()
    app.set_sensor_data()
    app.sort_sensor_data()
    beacon = app.find_beacon(limit)
    print(beacon)
    print(beacon[1]*4000000+beacon[0])

