from typing import List
from supply_stacks import get_cleaned_lines, create_crate_data, get_moves, get_top_crates

def make_move(crate_map:dict, move:List) -> None:
    """
    Given a dictionary of crate map and a list of move info, modifies the crate 
    map using CrateMover 9001 method.
    """
    crate_count = int(move[0])
    crate_map[move[1]], crates = crate_map[move[1]][:-crate_count], crate_map[move[1]][-crate_count:]
    crate_map[move[2]] += crates

if __name__ == '__main__':
    lines = get_cleaned_lines("5/supply_stacks.txt")
    crate_map, end_index = create_crate_data(lines)
    moves = get_moves(lines, end_index+2)
    for move in moves:
        make_move(crate_map, move)
    top_crates = get_top_crates(crate_map)
    print(top_crates)
        