from typing import List, Tuple
from helpers import get_matrix_max, print_matrix
from treetop import get_height_map

def get_left_distance(matrix:List[List], coordinate:Tuple, value:int) -> int:
    """
    Given a tree map and a coordinate, returns visible distance value in 'left' direction.
    """
    score = 0    
    i, j = coordinate
    while j > 0:
        score += 1
        if matrix[i][j-1] >= value:
            break
        j -= 1
    return score

def get_right_distance(matrix:List[List], coordinate:Tuple, value:int) -> int:
    """
    Given a tree map and a coordinate, returns visible distance value in 'right' direction.
    """
    score = 0    
    i, j = coordinate
    while j < len(matrix[0])-1:
        score += 1
        if matrix[i][j+1] >= value:
            break
        j += 1
    return score

def get_top_distance(matrix:List[List], coordinate:Tuple, value:int) -> int:
    """
    Given a tree map and a coordinate, returns visible distance value in 'top' direction.
    """
    score = 0    
    i, j = coordinate
    while i > 0:
        score += 1
        if matrix[i-1][j] >= value:
            break
        i -= 1
    return score

def get_bottom_distance(matrix:List[List], coordinate:Tuple, value:int) -> int:
    """
    Given a tree map and a coordinate, returns visible distance value in 'bottom' direction.
    """
    score = 0    
    i, j = coordinate
    while i < len(matrix)-1:
        score += 1
        if matrix[i+1][j] >= value:
            break
        i += 1
    return score

def get_scenic_score_map(matrix:List[List]) -> List[List]:
    """
    Given a 2d array of tree height map, generate and retruns a 2d array of scenic score map.
    """
    scenic_score_map = [[0 for i in range(99)] for i in range(99)]

    for i, row in enumerate(matrix[1:-1], start=1):
        for j, value in enumerate(row[1:-1], start=1):
            score = (
                get_left_distance(matrix, (i,j), value)
                *get_right_distance(matrix, (i,j), value)
                *get_top_distance(matrix, (i,j), value)
                *get_bottom_distance(matrix, (i,j), value)
            )
            scenic_score_map[i][j]=score

    return scenic_score_map

if __name__ == "__main__":
    tree_map = get_height_map(path="8/treetop.txt")
    scenic_score_map = get_scenic_score_map(tree_map)
    print_matrix(scenic_score_map)
    max_score = get_matrix_max(scenic_score_map)
    print(max_score)