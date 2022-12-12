from typing import List, Tuple
from helpers import print_matrix

class App():

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.map = []
        self.step_map = []
        self.step_list = []
        self.path = []
        self.start = ()
        self.step = 0
        self.finished = False

    def reset(self) -> None:
        """
        Resets app attributes.
        """
        self.step_map = []
        self.create_step_map()
        self.step_list = []
        self.path = []
        self.start = ()
        self.step = 0
        self.finished = False

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def get_char_value(self, char:str) -> int:
        """
        Given a character, returns value of the character, where 'a' is the 
        lowest elevation(0), 'b' is the next-lowest(1), and so on up to the 
        highest elevation, 'z'.
        """
        return ord(char) - 97

    def create_map(self) -> None:
        for i, line in enumerate(self.get_lines()):
            row = []
            for j, char in enumerate(line):
                if char == "S":
                    self.start = (i,j)
                    char = "a"
                if char == "E":
                    self.finish = (i,j)
                    char = "z"
                row.append(self.get_char_value(char))
            self.map.append(row)

    def create_step_map(self) -> None:
        """
        Creates a list of lists that represents a map to mark steps from start to finish.
        """
        self.step_map = [[-1 for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
        self.step_map[self.start[0]][self.start[1]] = 0

    def get_available_starts(self) -> List[Tuple]:
        """
        Finds and returns coordinates for 0 elevation points.
        """
        available_starts = []
        for i, row in enumerate(self.map):
            for j, value in enumerate(row):
                if value == 0:
                    available_starts.append((i,j))
        return available_starts

    def get_item_neighbors(self, item:Tuple) -> List[Tuple]:
        """
        Given acoordinate, looks neighbour cells, appends proper neighbors to 
        a list and returns the list.
        """
        neighbors = []
        i, j = item
        value = self.step_map[i][j]
        # left neighbor
        if j > 0:
            if self.step_map[i][j-1] == -1 and self.map[i][j]-self.map[i][j-1] >= -1:
                self.step_map[i][j-1] = value+1
                neighbors.append((i, j-1))
        # right neighbor
        if j < len(self.step_map[0]) - 1:
            if self.step_map[i][j+1] == -1 and self.map[i][j]-self.map[i][j+1] >= -1:
                self.step_map[i][j+1] = value+1
                neighbors.append((i, j+1))
        # up neighbor
        if i > 0:
            if self.step_map[i-1][j] == -1 and self.map[i][j]-self.map[i-1][j] >= -1:
                self.step_map[i-1][j] = value+1
                neighbors.append((i-1, j))
        # down neighbor
        if i < len(self.step_map) - 1:
            if self.step_map[i+1][j] == -1 and self.map[i][j]-self.map[i+1][j] >= -1:
                self.step_map[i+1][j] = value+1
                neighbors.append((i+1, j))
        return neighbors

    def find_neighbors(self, step:int) -> List[Tuple]:
        """
        Given a step number, finds and returns a list of neighbor coordinates 
        of the given step points.
        """
        neighbors = set()
        for item in self.step_list[step]:
            item_neighbors = self.get_item_neighbors(item)
            for neighbor in item_neighbors:
                neighbors.add(neighbor)
        return list(neighbors)

    def is_neighbor(self, item1:Tuple, item2:Tuple) -> bool:
        """
        Returns True if two items are neighbors. Otherwise returns False.
        """
        i1, j1 = item1
        i2, j2 = item2
        if i1 - i2 == 0 and abs(j1 - j2) == 1 or abs(i1 - i2) == 1 and j1 - j2 == 0:
            return True
        else:
            return False

    def make_path(self) -> List[Tuple]:
        """
        Creates and retuns a list of coordinates representing a path from start 
        to finish.
        """
        self.path = [self.finish]
        current = self.finish
        for step_items in self.step_list[-2::-1]:
            for item in step_items:
                if self.is_neighbor(current, item):
                    self.path.insert(0, item)
                    current = item
                    break
        return self.path


    def find_path(self) -> List[Tuple]:
        """
        Starts from start point and marks available moves for each step on step 
        map. After finding the finish point, create and returns the path from 
        start to finish if any solution available. If no solution returns an 
        empty list..
        """
        self.create_step_map()
        self.step_list.append([self.start])
        while not self.finished:
            neighbors = self.find_neighbors(self.step)
            if not neighbors:
                return [] # no solution
            if self.finish in neighbors:
                self.step_list.append([self.finish])
                return self.make_path()
            self.step_list.append(neighbors)
            self.step += 1

if __name__ == "__main__":
    app = App("12/hill_climbing.txt")
    app.create_map()
    start_points = app.get_available_starts()
    path_lengths = []
    for start_point in start_points:
        app.reset()
        app.start = start_point
        path = app.find_path()
        if not path:
            continue
        path_lengths.append(len(path)-1)
    print(min(path_lengths))
