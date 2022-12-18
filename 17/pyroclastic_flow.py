from typing import List, Tuple, Any
from helpers import print_matrix
from models import RockDash, RockL, RockPlus, RockStick, RockSquare
from itertools import cycle

class App():
    def __init__(self, file_path, rock_qty, *args, **kwargs) -> None:
        self.file_path = file_path
        self.rock_qty = rock_qty
        self.map:List[List[str]] = []
        self.top_level:int = 0
        self.rocks = cycle([RockDash, RockPlus, RockL, RockStick, RockSquare])
        self.pattern = None
        self.landed = False
        self.current_rock = None
        self.move_count = 0

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def create_map(self) -> None:
        """
        Creates a 2d array that represents the tall and narrow chamber.
        """
        self.map = [["." for item in range(7)] for row in range(10)]

    def create_pattern(self):
        self.pattern = cycle(next(self.get_lines()))

    def setup(self) -> None:
        """
        Creates map, 
        """
        self.create_map()
        self.create_pattern()

    def create_rock(self) -> None:
        """
        Creates a rock using the next rock class and assign as current rock.
        """
        rock_class = next(self.rocks)
        offset = (self.top_level+3, 2)
        self.current_rock = rock_class(offset)

    def rock_can_move_left(self) -> bool:
        """
        Checks if the current rock can move left.
        """
        for point in self.current_rock.get_left_points():
            y, x = point
            if x < 0:
                return False
            if self.map[y][x] == "#":
                return False
        return True
        
    def rock_can_move_right(self) -> bool:
        """
        Checks if the current rock can move right.
        """
        for point in self.current_rock.get_right_points():
            y, x = point
            if x > 6:
                return False
            if self.map[y][x] == "#":
                return False
        return True

    def rock_can_move_down(self) -> bool:
        """
        Checks if the current rock can move down.
        """
        for point in self.current_rock.get_landing_points():
            y, x = point
            if y < 0:
                return False
            if self.map[y][x] == "#":
                return False
        return True

    def push_rock(self) -> None:
        """
        Pushes the rock left or right due to next input command.
        """
        self.move_count += 1
        move = next(self.pattern)
        y, x = self.current_rock.offset
        if move == "<":
            if self.rock_can_move_left():
                self.current_rock.offset = (y, x-1)
        elif move == ">":
            if self.rock_can_move_right():
                self.current_rock.offset = (y, x+1)
        else: 
            raise ValueError("Invalid push command!")

    def fall_rock(self) -> None:
        """
        Moves the rock down if the rock can move down.
        """
        if self.rock_can_move_down():
            y, x = self.current_rock.offset
            self.current_rock.offset = (y-1, x)
        else:
            self.landed = True

    def place_rock_on_map(self) -> None:
        """
        Marks the final posiition of rock on the map.
        """
        offset = self.current_rock.offset
        for j, row in enumerate(self.current_rock.pattern):
            for i, item in enumerate(row):
                if item == "#":
                    self.map[j+offset[0]][i+offset[1]] = item

    def add_blank_levels_to_map(self, qty:int) -> None:
        """
        Adds blank rows to map in given quantity.
        """
        self.map += [["." for _ in range(7)] for row in range(qty)]

    def update_top_level(self) -> None:
        """
        After a rock is placed, checks the map, finds and updates new top level.
        """
        for i in range(5):
            if '#' not in self.map[self.top_level+i]:
                self.top_level += i
                if i:
                    self.add_blank_levels_to_map(i)
                break

    def run(self):
        """
        Runs the simulation loop.
        """
        for _ in range(self.rock_qty):
            self.create_rock()
            while not self.landed:
                self.push_rock()
                self.fall_rock()
            self.place_rock_on_map()
            self.update_top_level()
            self.landed = False      

def main(qty):
    rock_qty = qty
    file_path = "17/pyroclastic_flow.txt"
    # file_path = "17/test_input.txt"
    app = App(file_path, rock_qty)
    app.setup()
    app.run()
    return app.move_count, app.top_level

def solve(a:int, b:int, total_rock_qty:int) -> int:
    c = (total_rock_qty - a)%b
    top_level_a = main(a)[1]
    pattern_level = main(a+b)[1] - top_level_a
    top_level_c = main(a+c)[1] - top_level_a
    pattern_repetation = (total_rock_qty-a-c)//b
    max_level = top_level_a + (pattern_repetation*pattern_level) + top_level_c
    print(a, b, c)
    print(top_level_a, pattern_level, top_level_c, pattern_repetation, max_level)

if __name__ == "__main__":
    total_rock_qty = 1000000000000
    # total_rock_qty = 2022
    # part1
    print(main(2022)[1])

    # part2
    qty = 5
    pattern_check = ""
    previous_count = 0
    while True:
        move_count = main(qty)
        pattern_check += str(move_count[0]-previous_count)
        if pattern_check[-12:] in pattern_check[:-12]:
            a = int(pattern_check.find(pattern_check[-12:])/2*5) # blocks before repeted pattern
            b = int(pattern_check.rfind(pattern_check[-12:])/2*5) - a # number of blocks in pattern
            solve(a, b, total_rock_qty)
            break
        previous_count = move_count[0]
        qty += 5