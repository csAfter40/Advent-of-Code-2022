from typing import Tuple
from camp_cleanup import get_pair

def is_overlapping(pair: Tuple[Tuple[int]]) -> bool:
    """
    Given a tuple of pair info, checks if any Elf's assignment overlaps the other.
    """
    return not (
        pair[0][1] < pair[1][0] or pair[1][1] < pair[0][0]
    )

if __name__ == "__main__":
    with open('4/camp_cleanup.txt') as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            pair = get_pair(line)
            if is_overlapping(pair):
                total += 1
        print(total)