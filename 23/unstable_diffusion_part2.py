from typing import List, Dict, Tuple, Set
from helpers import print_matrix
from itertools import cycle

class App():
    def __init__(self, file_path:str, check_round:int=None, *args, **kwargs) -> None:
        self.file_path = file_path
        self.check_round = check_round
        self.data:List[List[int]]
        self.elves:Set[Tuple[int]] = set()
        self.directions = cycle(
            (
                (-1, 0), #N
                (1, 0), #S
                (0, -1), #W
                (0, 1), #E
            )
        )

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def extract_data(self) -> List[List[int]]:
        """
        Reads file and creates a data array representing a map of elves. Returns the data array.
        """
        data = []
        for line in self.get_lines():
            row = []
            for char in line:
                row.append(char)
            data.append(row)
        self.data = data

    def create_elves(self) -> None:
        """
        Reads the map and create elves.
        """
        for y, row in enumerate(self.data):
            for x, value in enumerate(row):
                if value == "#":
                    self.elves.add((y, x))

    def setup(self) -> None:
        """
        Setup data structure.
        """
        self.extract_data()
        self.create_elves()

    def get_map_size(self) -> Tuple:
        """
        Looks for the min and max coordinate for elves and returns size of a 
        rectangle surrounding the elves and a vector of offset from (0, 0).
        """
        any_elf = next(iter(self.elves))
        min_y = max_y = any_elf[0]
        min_x = max_x = any_elf[1]
        for elf in self.elves:
            if elf[0] < min_y:
                min_y = elf[0]
            if elf[0] > max_y:
                max_y = elf[0]
            if elf[1] < min_x:
                min_x = elf[1]
            if elf[1] > max_x:
                max_x = elf[1]
        size = (max_y-min_y+1, max_x-min_x+1)
        offset = (-min_y, -min_x)
        return size, offset

    def get_map(self) -> List[List[int]]:
        """
        Given list of elves, creates and returns a map.
        """
        size, offset = self.get_map_size()
        map = [["." for _ in range(size[1])] for row in range(size[0])]
        for elf in self.elves:
            pos = self.add_arrays(elf, offset)
            map[pos[0]][pos[1]] = "#"
        return map

    def get_next_direction(self, direction:Tuple[int]) -> Tuple[int]:
        """
        Given a direction, returns the next direction on the queue. Returns None 
        if next directionis the direction of the round.
        """
        directions = {
            (-1, 0): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (0, 1),
            (0, 1): (-1, 0)
        }
        new_direction = directions[direction]
        return new_direction if new_direction != self.direction else None

    def add_arrays(self, a1:Tuple[int], a2:Tuple[int]) -> Tuple[int]:
        """
        Adds 2 arrays and returns the result.
        """
        a1_y, a1_x = a1
        a2_y, a2_x = a2
        return (a1_y+a2_y, a1_x+a2_x)

    def is_distinct(self, elf:Tuple[int]) -> bool:
        """
        Checks if the elf is not adjacent with other elves.
        """
        adjacent_cells = (
            (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
        )
        for cell in adjacent_cells:
            if self.add_arrays(elf, cell) in self.elves:
                return False
        return True

    def get_next_position(self, elf:Tuple[int], direction:Tuple[int]) -> Tuple[int]:
        """
        Given an elf and a direction, checkes the adjacent cells in the 
        direction and neighbors and returns the coordinates of the cell 
        if no elves on the way.
        """
        if self.is_distinct(elf):
            return None
        pos_y, pos_x = elf
        dir_y, dir_x = direction
        if dir_y == 0:
            cells = (
                (pos_y+dir_y, pos_x+dir_x), 
                (pos_y+dir_y-1, pos_x+dir_x), 
                (pos_y+dir_y+1, pos_x+dir_x), 
            )
        else:
            cells = (
                (pos_y+dir_y, pos_x+dir_x), 
                (pos_y+dir_y, pos_x+ dir_x-1), 
                (pos_y+dir_y, pos_x+dir_x+1), 
            )
        for cell in cells:
            if cell in self.elves:
                next_direction = self.get_next_direction(direction)
                if next_direction:
                    return self.get_next_position(elf, next_direction)
                else:
                    return None
        return (pos_y+dir_y, pos_x+dir_x)

    def get_proposes(self, direction:Tuple[int]) -> Dict:
        """
        For given direction, traverses through the elves and returns a dictionary 
        of proposes.
        """
        elves = {}
        proposes = {}
        for elf in self.elves:
            next_position = self.get_next_position(elf, direction)
            if next_position == None:
                continue
            elif next_position not in proposes:
                elves[elf] = next_position
                proposes[next_position] = elf
            else:
                if elves[proposes[next_position]]:
                    elves.pop(proposes[next_position])
        return elves

    def move_elves(self, elves:Dict) -> None:
        """
        Update all the elf coordinates with the new coordinates in the dictionary
        and updates elves list of the class.
        """
        for elf, propose in elves.items():
            self.elves.remove(elf)
            self.elves.add(propose)

    def run(self) -> None:
        # for round in range(self.check_round):
        round_count = 0
        while True:
            round_count += 1
            # First half
            self.direction = next(self.directions)
            available_elves = self.get_proposes(self.direction)
            if not available_elves:
                break
            # Second half
            self.move_elves(available_elves)
        print(f"All elves are distinct after {round_count} rounds")

    def get_empty_tiles_qty(self) -> int:
        """
        Counts and returns the quantity of empty tiles on map.
        """
        map = self.get_map()
        count = 0
        for row in map:
            for item in row:
                if item == ".":
                    count += 1
        return count

if  __name__ == "__main__":
    file_path = "23/unstable_diffusion.txt"
    # file_path = "23/test_input.txt"
    app = App(file_path)
    app.setup()
    app.run()
    empty_tiles_qty = app.get_empty_tiles_qty()