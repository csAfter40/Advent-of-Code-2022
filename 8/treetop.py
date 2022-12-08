from typing import List
from helpers import get_matrix_sum

def get_lines(path:str) -> List[str]:
    """
    Reads the file at given path and return cleaned lines as an array.
    """
    with open(path) as f:
        return [line.rstrip("\n") for line in f.readlines()]

def get_height_map(path:str) -> List[List]:
    """
    Given a file path, returns values as 2d array of integers.
    """
    lines = get_lines(path)
    return [[int(char) for char in line] for line in lines]

def get_visible_map(matrix:List[List]) -> List[List]:
    """
    Given an array of tree heights map, returns a 2d array of visible tree map.
    """
    visible_map = [[0 for i in range(99)] for i in range(99)]
    # left
    for i, row in enumerate(matrix):
        max_height = -1
        for j, value in enumerate(row):
            if value>max_height:
                visible_map[i][j] = 1
                max_height = value
            if value == 9:
                break

    #right
    for i, row in enumerate(matrix):
        max_height = -1
        for j, value in reversed(list(enumerate(row))):
            if value>max_height:
                visible_map[i][j] = 1
                max_height = value
            if value == 9:
                break

    #top
    for j in range(len(matrix[0])):
        max_height = -1
        for i in range(len(matrix)):
            if matrix[i][j]>max_height:
                visible_map[i][j] = 1
                max_height = matrix[i][j]
            if value == 9:
                break
        
    #bottom
    for j in range(len(matrix[0])):
        max_height = -1
        for i in reversed(range(len(matrix))):
            if matrix[i][j]>max_height:
                visible_map[i][j] = 1
                max_height = matrix[i][j]
            if value == 9:
                break

    return visible_map

if __name__ == "__main__":
    tree_map = get_height_map(path="8/treetop.txt")
    visible_map = get_visible_map(tree_map)
    visible_sum = get_matrix_sum(visible_map)
    print(visible_sum)