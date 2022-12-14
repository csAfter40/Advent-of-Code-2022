from typing import List, Tuple, Any
from helpers import print_matrix

class Cave():
    def __init__(self, map:List[List]) -> None:
        self.map = map
        self.overflow = False

    def get_sands(self) ->List[List]:
        """
        Returns a list of sand coordinates inside the cave.
        """
        sands = []
        for row in self.map:
            for item in row:
                if isinstance(item, Sand):
                    sands.append(item)
        return sands

    def get_sand_qty(self) -> int:
        """
        Returns quantity of sand inside the cave.
        """
        return len(self.get_sands)

    def print_map(self) -> None:
        """
        Prints map on console.
        """
        print_matrix(self.map)
    
class Rock():
    def __init__(self, cave:Cave) -> None:
        self.cave = cave

    def __repr__(self) -> str:
        return "#"

class Air():
    def __init__(self, cave:Cave) -> None:
        self.cave = cave
    def __repr__(self) -> str:
        return "."

class Sand():
    def __init__(self, location:Tuple[int], cave:Cave) -> None:
        self.location = location
        self.cave = cave
        self.free = True

    def __repr__(self) -> str:
        return "o"

    def add_sand_to_cave(self) -> None:
        """
        Adds sand to cave's sand list.
        """
        self.cave.sands.append(self.location)

    def move(self) -> Tuple[int]:
        """
        Calculates and returns next position of sand.
        """
        i, j = self.location
        if i == len(self.cave.map)-1:
            self.free = False
            self.cave.overflow = True
        elif isinstance(self.cave.map[i+1][j], Air):
            self.location = (i+1, j)
        elif j == 0:
            self.free = False
            self.cave.overflow = True
        elif isinstance(self.cave.map[i+1][j-1], Air):
            self.location = (i+1, j-1)
        elif j == len(self.cave.map[0])-1:
            self.free = False
            self.cave.overflow = True
        elif isinstance(self.cave.map[i+1][j+1], Air):
            self.location = (i+1, j+1)
        else:
            self.free = False
            self.cave.map[i][j] = self

    def run(self) -> None:
        """
        Runs sand until it is stopped.
        """
        while self.free:
            self.move()



class App():
    def __init__(self, file_path:str, sand_source:Tuple[int]) -> None:
        self.file_path = file_path
        self.sand_source = sand_source
        self.cave: Cave = None
        self.commands: List[List] = []
        self.set_commands()

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def set_commands(self) -> None:
        """
        Reads lines, formats data and stores in commands list:
        """
        for line in self.get_lines():
            command = [tuple(reversed([int(i) for i in item.split(",")])) for item in line.split("->")]
            self.commands.append(command)

    def get_map_dimensions(self) -> Tuple:
        """
        Calculates and returns map dimensions.
        """
        initials = self.sand_source
        h_min = initials[1]
        h_max = initials[1]
        v_min = initials[0]
        v_max = initials[0]
        for command in self.commands:
            for item in command:
                if item[1] < h_min:
                    h_min = item[1]
                if item[1] > h_max:
                    h_max = item[1]
                if item[0] < v_min:
                    v_min = item[0]
                if item[0] > v_max:
                    v_max = item[0]
        dimensions = (v_max-v_min+1, h_max-h_min+1)
        offset = (v_min, h_min)
        return dimensions, offset

    def create_map_template(self, dimensions:Tuple) -> List[List]:
        """
        Given dimensions, creates and returns a 2d array representing template 
        for a cave map.
        """
        empty_map = []
        for i in range(dimensions[0]):
            row = []
            for j in range(dimensions[1]):
                row.append(Air(self.cave))
            empty_map.append(row)
        return empty_map

    def offset_sand_source(self, offset:Tuple) -> None:
        """
        Given offset info, offset sand source position on map.
        """
        self.sand_source = (self.sand_source[0]-offset[0], self.sand_source[1]-offset[1])

    def put_item_on_map(self, item:Any, coordinates:Tuple[int]) -> None:
        """
        Puts given item on map on given coordinates.
        """
        self.cave.map[coordinates[0]][coordinates[1]] = item

    def calculate_rock_locations(self, command:List[Tuple]) -> List[Tuple]:
        """
        Given command, calculates rock coordinates and returns list of all 
        rock coordinates in the command.
        """
        rock_locations = []
        for i, item in enumerate(command[1:], start=1):
            if item[0] - command[i-1][0] == 0:
                len = abs(item[1] - command[i-1][1])
                direction = 1 if item[1]-command[i-1][1]<0 else -1
                for j in range(len+1):
                    location = (item[0], item[1]+direction*j)
                    rock_locations.append(location)
            else:
                len = abs(item[0] - command[i-1][0])
                direction = 1 if item[0]-command[i-1][0]<0 else -1
                for j in range(len+1):
                    location = (item[0]+direction*j, item[1])
                    rock_locations.append(location)
        return rock_locations

    def offset_commands(self, offset:Tuple) -> None:
        """
        Given offset info, offsets all coordinates in commnads.
        """
        for i, command in enumerate(self.commands):
            for j, item in enumerate(command):
                self.commands[i][j] = (item[0]-offset[0], item[1]-offset[1])

    def create_map(self) -> List[List]:
        """
        Creates a 2d array representing map of cave using commands.
        """
        dimensions, offset = self.get_map_dimensions()
        self.offset_sand_source(offset)
        map = self.create_map_template(dimensions)
        map[self.sand_source[0]][self.sand_source[1]] = "+"
        self.offset_commands(offset)
        for command in self.commands:
            rock_locations = self.calculate_rock_locations(command)
            for location in rock_locations:
                map[location[0]][location[1]] = Rock(self.cave)
        return map


    def create_cave(self) -> None:
        """
        Creates a map and a cave instance.
        """
        map = self.create_map()
        self.cave = Cave(map)

    def pour_sand(self) -> None:
        """
        Pours sand from sand source until maximum quantity of sand is achieved 
        on map.
        """
        while not self.cave.overflow:
            sand = Sand(self.sand_source, self.cave)
            sand.run()


if __name__ == "__main__":
    # file_path = "14/test_input.txt"
    file_path = "14/regolith.txt"
    sand_source = (0,500)
    app = App(file_path, sand_source)
    map = app.create_cave()
    app.pour_sand()
    app.cave.print_map()
    print(f"Sand quantity: {len(app.cave.get_sands())} units")