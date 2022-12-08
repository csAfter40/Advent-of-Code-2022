from typing import List

def print_matrix(matrix:List[List]) -> None:
    """
    Prints a given 2d array on console without commas and brackets.
    """
    for row in matrix:
        print(*row, sep="") 

def get_matrix_sum(matrix:List[List[int]]) -> int:
    """
    Given a 2d array, traverses the array and returns the sum of all values. 
    """
    return sum([sum(row) for row in matrix])

def get_matrix_max(matrix:List[List[int]]) -> int:
    """
    Given a 2d array, traverses the array and returns the maximum value. 
    """
    return max([max(row) for row in matrix])