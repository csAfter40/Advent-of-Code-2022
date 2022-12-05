from typing import List, Tuple

def get_cleaned_lines(path:str) -> List[str]:
    """
    Given a path, reads the file and returns lines in the file as a list of string.
    """
    with open(path) as f:
        lines = f.readlines()
        return [line.rstrip("\n") for line in lines]

def create_crate_data(lines:List[str]) -> Tuple[dict, int]:
    """
    Given a list of strings, returns a dictionary in which keys are stacks 
    and values are string representation of crates in the stack and an integer 
    representing ending line index of crate data.
    example: {'1': 'GTRW', '2': 'GCHPMSVW', '3': 'CLTSGM'}, 9
    """
    data = {}
    stacks = ""
    crates = []
    end_index = 0
    for i, line in enumerate(lines):
        if "1" in line:
            stacks = line
            end_index = i
            break
        crates.insert(0, line)
    for i, stack in enumerate(stacks):
        if not stack.isspace():
            data[stack] = ''.join([crate[i] for crate in crates]).rstrip()
    return data, end_index

def get_moves(lines:List[str], index:int) -> List[List]:
    """
    Given a list of strings and an index number, extracts crate movements and returns a list of lists.
    """
    moves = []
    for line in lines[index:]:
        move = line.split()[1:6:2]
        moves.append(move)
    return moves 

def make_move(crate_map:dict, move:List) -> None:
    """
    Given a dictionary of crate map and a list of move info, modifies the crate map.
    """
    for i in range(int(move[0])):
        crate_map[move[1]], char = crate_map[move[1]][:-1], crate_map[move[1]][-1]
        crate_map[move[2]] += char

def get_top_crates(crate_map:dict) -> str:
    """
    Given a dictionary of crate map, returns a string representation of the 
    crates at the top of each stack.
    """
    result = ""
    for i in range(len(crate_map)):
        result += crate_map[str(i+1)][-1]
    return result

if __name__ == '__main__':
    lines = get_cleaned_lines("5/supply_stacks.txt")
    crate_map, end_index = create_crate_data(lines)
    moves = get_moves(lines, end_index+2)
    for move in moves:
        make_move(crate_map, move)
    top_crates = get_top_crates(crate_map)
    print(top_crates)

        