from typing import List, Tuple
from helpers import get_matrix_sum

KNOT_QTY = 9 # 1 for problem part1 and 9 for problem part2

def get_lines(path:str) -> List[str]:
    """
    Reads the file at given path and return cleaned lines as an array.
    """
    with open(path) as f:
        return [line.rstrip("\n") for line in f.readlines()]

def get_moves(path:str) -> List[Tuple]:
    """
    Given a file path, returns list of moves.
    """
    lines = get_lines(path)
    moves = []
    for line in lines:
        move_couple = line.split()
        moves.append((move_couple[0], int(move_couple[1])))
    return moves

def get_knots(knot_qty:int, start_pos:Tuple) -> List[Tuple]:
    """
    Given quantity of knots, returns a list of coordinates for knots which is 
    (0, 0) for all.
    """
    return [start_pos for i in range(knot_qty)]

def get_min_max_positions(head_positions:List[Tuple]) -> Tuple:
    """
    Given list of head positions, returns a tuple of maximum and minimum x and 
    y axis positions. returns (x_max, x_min, y_max, y_min)
    """
    x_positions = [position[1] for position in head_positions]
    y_positions = [position[0] for position in head_positions]
    x_max = max(x_positions)
    x_min = min(x_positions)
    y_max = max(y_positions)
    y_min = min(y_positions)
    return x_max, x_min, y_max, y_min

def create_matrix(dimensions:Tuple) -> Tuple:
    """
    Creates and returns a zero matrix of given dimensions.
    """
    return [[0 for i in range(dimensions[1])] for i in range(dimensions[0])]

def get_matrix(moves:List[Tuple]) -> List[List]:
    """
    Given list of moves, calculates move spans and returns a zero matrix of and 
    starting point of movements.
    """
    head_positions = [(0,0)]
    for move in moves:
        j, i = head_positions[-1]
        if move[0] == 'R':
            head_positions.append((j, i+move[1]))
        if move[0] == 'L':
            head_positions.append((j, i-move[1]))
        if move[0] == 'U':
            head_positions.append((j+move[1], i))
        if move[0] == 'D':
            head_positions.append((j-move[1], i))
    extremums = get_min_max_positions(head_positions)
    x_max, x_min, y_max, y_min = extremums
    matrix = create_matrix((y_max-y_min+1, x_max-x_min+1))
    start = (y_max, -x_min)
    matrix[start[0]][start[1]] = 1 #mark starting point
    return matrix, start

def get_new_head_pos(current_pos:Tuple[int], direction:str) -> Tuple[int]:
    """
    Given a position and a move info, returns new position of the head. 
    """
    i, j = current_pos
    if direction == "R":
        j += 1
    if direction == "L":
        j -= 1
    if direction == "D":
        i += 1
    if direction == "U":
        i -= 1
    return i, j

def get_distance(knot:Tuple[int], target:Tuple[int]) -> int:
    """
    Given tail and head positions, calculates and returns distance between 
    tail and head according to rules.
    """
    return max(abs(target[0]-knot[0]), abs(target[1]-knot[1]))

def move_knot(knot:Tuple, target:Tuple) -> Tuple:
    """
    Given knot and target(head or previous knot) positions, calculate and 
    returns new knot position.
    """
    ki, kj = knot
    ti, tj = target
    distance_i = abs(ti - ki)
    distance_j = abs(tj - kj)
    if distance_i == 1:
        ki = ti
    if distance_i == 2:
        ki = int((ki+ti)/2)
    if distance_j == 1:
        kj = tj
    if distance_j == 2:
        kj = int((kj+tj)/2)
    return ki, kj

def move_knots(knots:List[Tuple], head:Tuple) -> List[Tuple]:
    """
    Given knots and head postions, returns new knots positions.
    """
    target = head
    for i, knot in enumerate(knots):
        distance = get_distance(knot, target)
        if distance > 2:
            raise Exception
        if distance == 2:
            knots[i] = move_knot(knot, target)
        else:
            break
        target = knots[i]
    return knots

def make_moves(moves:List[Tuple], matrix:List[List], start:Tuple) -> List[List]:
    """
    Given list of head moves, a map for marking tail positions and start node 
    position, creates a list of knots and calculate position of knots due to 
    moves. Marks tail position for each increment of a move and returns the map.
    """
    head = start
    knots = get_knots(KNOT_QTY, start)
    for move in moves:
        direction, displacement = move
        for _ in range(displacement):
            head = get_new_head_pos(head, direction)
            knots = move_knots(knots, head)
            matrix[knots[-1][0]][knots[-1][1]] = 1
    return matrix

if __name__ == "__main__":
    moves = get_moves("9/rope_bridge.txt")
    matrix, start = get_matrix(moves)
    tail_map = make_moves(moves, matrix, start)
    print(get_matrix_sum(tail_map))