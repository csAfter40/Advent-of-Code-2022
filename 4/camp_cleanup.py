from typing import Tuple

def get_pair(line:str) -> Tuple[Tuple[int]]:
    """
    Given a string of pair info, returns a tuple of tuple of integers which has section assignments info for eacf Elf.
    """
    return (
        tuple(map(int, line.strip().split(',')[0].split('-'))),
        tuple(map(int, line.strip().split(',')[1].split('-')))
    )

def is_containing(pair: Tuple[Tuple[int]]) -> bool:
    """
    Given a tuple of pair info, checks if any Elf's assignment fully contains the other.
    """
    return (
        (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]) or 
        (pair[1][0] <= pair[0][0] and pair[1][1] >= pair[0][1])
    )

if __name__ == "__main__":
    with open('4/camp_cleanup.txt') as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            pair = get_pair(line)
            if is_containing(pair):
                total += 1
        print(total)