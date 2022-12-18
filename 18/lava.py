from typing import List, Tuple, Set, Any
import math

class App():
    def __init__(self, file_path, *args, **kwargs) -> None:
        self.file_path = file_path
        self.cubes:Set[Tuple[int]] = set()
        self.neighbors:Set[Tuple[int]] = set()
        self.bubble_cells:Set[Tuple[int]] = set()
        self.outer_cells:Set[Tuple[int]] = set()
        self.currently_searching:Set[Tuple[int]] = set()

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def set_cubes(self) -> None:
        """
        Parses the given data.
        """
        for line in self.get_lines():
            cube = tuple([int(value) for value in line.split(",")])
            self.cubes.add(cube)

    def calculate_area(self, cube:Tuple[int], outer) -> int:
        """
        Given a cube, returns the sum of empty faces.
        """
        z, y, x = cube
        neighbor_offsets = {
            (1,0,0),
            (0,1,0),
            (0,0,1),
            (-1,0,0),
            (0,-1,0),
            (0,0,-1),
        }
        surface_area = 0
        for neighbor_offset in neighbor_offsets:
            k, j, i = neighbor_offset
            neighbor = (z+k, j+y, i+x)
            if outer:
                if neighbor not in self.cubes and neighbor not in self.bubble_cells:
                    surface_area += 1
                    self.neighbors.add(neighbor)
            elif neighbor not in self.cubes:
                surface_area += 1
                self.neighbors.add(neighbor)
        return surface_area

    def find_surface_area(self, outer=False) -> int:
        """
        Traverses through the given cubes and finds the number of total empty faces.
        """
        total_area = 0
        for cube in self.cubes:
            area = self.calculate_area(cube, outer)
            total_area += area
        return total_area

    def setup(self) -> None:
        """
        Sets up the app.
        """
        self.set_cubes()
        self.calculate_biggest_bubble()

    def calculate_biggest_bubble(self) -> None:
        """
        Calculates the biggest bubble size possible for a given list of cubes. 
        Needed to be used as a boundary for depth search.
        """
        surface = len(self.cubes)
        self.biggest_bubble_size = int((surface**1.5)/(6*math.pi**0.5))

    def get_empty_neighbors(self, cell:Tuple[int]) -> List[Tuple[int]]:
        """
        Given a cell, finds and returns empty and not visited before neighbors.
        """
        z, y, x = cell
        neighbor_offsets = {
            (1,0,0),
            (0,1,0),
            (0,0,1),
            (-1,0,0),
            (0,-1,0),
            (0,0,-1),
        }
        empty_neighbors = []
        for neighbor_offset in neighbor_offsets:
            k, j, i = neighbor_offset
            neighbor = (z+k, j+y, i+x)
            if neighbor not in self.cubes and neighbor not in self.currently_searching:
                empty_neighbors.append(neighbor)
        return empty_neighbors

    def search_around(self, neighbors:List[Tuple[int]]) -> Tuple[Any]:
        """
        Given a list of cells, searches around and finds if they are a part of a 
        bubble or not. Returns list of cells and a boolean.
        """
        group = set(neighbors)
        new_neighbors = set()
        for neighbor in neighbors:
            if len(group) > self.biggest_bubble_size:
                return group, False
            empties = self.get_empty_neighbors(neighbor)
            new_neighbors.update(empties)
            for empty in empties:
                if empty in self.outer_cells:
                    group.update(new_neighbors)
                    return group, False
        if not new_neighbors:
            return group, True
        self.currently_searching.update(new_neighbors)
        if len(self.currently_searching) > self.biggest_bubble_size:
            return group, False
        new_group, is_bubble = self.search_around(new_neighbors)
        group.update(new_group)
        return group, is_bubble

    def find_bubbles(self) -> None:
        """
        Beginnig from a neighbor cell, searches through the adjecent cells and 
        group cells as bubble cells or outer cells.
        """
        for neighbor in self.neighbors:
            if neighbor in self.bubble_cells or neighbor in self.outer_cells:
                continue
            self.currently_searching = set()
            group, is_bubble = self.search_around([neighbor])
            if is_bubble:
                self.bubble_cells.update(group)
            else:
                self.outer_cells.update(group)

    def mark_outermost_cells(self) -> None:
        """
        Finds outermost cells of given input and adds them to outer cells set.
        """
        initial = next(iter(self.cubes))
        z_max, y_max, x_max = initial
        z_min, y_min, x_min = initial
        z_max_cells = []
        z_min_cells = []
        y_max_cells = []
        y_min_cells = []
        x_max_cells = []
        x_min_cells = []

        for cell in self.neighbors:
            z, y, x = cell
            if z > z_max:
                z_max = z
                z_max_cells = [cell]
            elif z == z_max:
                z_max_cells.append(cell)
            if z < z_min:
                z_min = z
                z_min_cells = [cell]
            elif z == z_min:
                z_min_cells.append(cell)

            if y > y_max:
                y_max = y
                y_max_cells = [cell]
            elif y == y_max:
                y_max_cells.append(cell)
            if y < y_min:
                y_min = y
                y_min_cells = [cell]
            elif y == y_min:
                y_min_cells.append(cell)

            if x > x_max:
                x_max = x
                x_max_cells = [cell]
            elif x == x_max:
                x_max_cells.append(cell)
            if x < x_min:
                x_min = x
                x_min_cells = [cell]
            elif x == x_min:
                x_min_cells.append(cell)
        self.outer_cells.update(z_max_cells+z_min_cells+y_max_cells+y_min_cells+x_max_cells+x_min_cells)

if __name__ == "__main__":
    # file_path = "18/test_input.txt"
    file_path = "18/lava.txt"
    app = App(file_path)
    app.setup()
    surface_area = app.find_surface_area()
    print(f"Surface area is {surface_area}")

    # part 2
    app.mark_outermost_cells()
    app.find_bubbles()
    surface_area = app.find_surface_area(outer=True)
    print(f"Outer surface area is {surface_area}")