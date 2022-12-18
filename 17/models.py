from typing import Tuple, List

class RockDash():
    def __init__(self, offset:Tuple[int], *args, **kwargs):
        self.pattern = [
            ["#", "#", "#", "#"]
        ]
        self.offset: Tuple[int] = offset

    def get_landing_points(self) -> List[Tuple[int]]:
        y, x = self.offset
        return [(y-1, x), (y-1, x+1), (y-1, x+2), (y-1, x+3)]

    def get_right_points(self):
        y, x = self.offset
        return [(y, x+4)]
    
    def get_left_points(self):
        y, x = self.offset
        return [(y, x-1)]

class RockPlus():
    def __init__(self, offset:Tuple[int], *args, **kwargs):
        self.pattern = [
            [".", "#", "."],
            ["#", "#", "#"],
            [".", "#", "."],
        ]
        self.offset: Tuple[int] = offset

    def get_landing_points(self) -> List[Tuple[int]]:
        y, x = self.offset
        return [(y, x), (y-1, x+1), (y, x+2)]

    def get_right_points(self):
        y, x = self.offset
        return [(y, x+2), (y+1, x+3), (y+2, x+2)]
    
    def get_left_points(self):
        y, x = self.offset
        return [(y, x), (y+1, x-1), (y+2, x)]
        

class RockL():
    def __init__(self, offset:Tuple[int], *args, **kwargs):
        self.pattern = [
            ["#", "#", "#"],
            [".", ".", "#"],
            [".", ".", "#"],
        ]
        self.offset: Tuple[int] = offset

    def get_landing_points(self) -> List[Tuple[int]]:
        y, x = self.offset
        return [(y-1, x), (y-1, x+1), (y-1, x+2)]

    def get_right_points(self):
        y, x = self.offset
        return [(y, x+3), (y+1, x+3), (y+2, x+3)]
    
    def get_left_points(self):
        y, x = self.offset
        return [(y, x-1), (y+1, x+1), (y+2, x+1)]

class RockStick():
    def __init__(self, offset:Tuple[int], *args, **kwargs):
        self.pattern = [
            ['#'],
            ['#'],
            ['#'],
            ['#']
        ]
        self.offset: Tuple[int] = offset

    def get_landing_points(self) -> List[Tuple[int]]:
        y, x = self.offset
        return [(y-1, x)]

    def get_right_points(self):
        y, x = self.offset
        return [(y, x+1), (y+1, x+1), (y+2, x+1), (y+3, x+1)]
    
    def get_left_points(self):
        y, x = self.offset
        return [(y, x-1), (y+1, x-1), (y+2, x-1), (y+3, x-1)]
        
class RockSquare():
    def __init__(self, offset:Tuple[int], *args, **kwargs):
        self.pattern = [
            ['#', '#'],
            ['#', '#']
        ]
        self.offset: Tuple[int] = offset

    def get_landing_points(self) -> List[Tuple[int]]:
        y, x = self.offset
        return [(y-1, x), (y-1, x+1)]

    def get_right_points(self):
        y, x = self.offset
        return [(y, x+2), (y+1, x+2)]
    
    def get_left_points(self):
        y, x = self.offset
        return [(y, x-1), (y+1, x-1)]
        