from typing import List

class NoCommonItemsError(Exception):
    """
    Raises when no common item found on two compartments of a rucksack.
    """
    def __init__(self, message="No common items found"):
        self.message = message
        super().__init__(self.message)

def get_priority(char:str) -> int:
    """
    Given a character, returns a priority number based on the rules below:    
    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
 
    """
    if char.islower():
        return ord(char) - 96
    return ord(char) - 38

def get_share_item(items:str) -> str:
    """
    Given a string , finds and retuns the common character between first half and second half of the string.
    """
    second_comp_items = set(items[len(items)//2:])
    for item in items[:len(items)//2]:
        if item in second_comp_items:
            return item
    raise NoCommonItemsError

def get_group_item(rucksacks:List[str]) -> str:
    """
    Given a list of strings with len = 3, returns the common character in all strings in the list. 
    """
    second_rucksack = set(rucksacks[1])
    third_rucksack = set(rucksacks[2])
    for item in rucksacks[0]:
        if item in second_rucksack and item in third_rucksack:
            return item
    raise NoCommonItemsError

if __name__ == '__main__':
    with open('3/rucksack.txt') as f:
        lines = f.readlines()
        total = 0
        for i in range(0,len(lines),3):
            rucksacks = lines[i:i+3]
            item = get_group_item(rucksacks)
            priority = get_priority(item)
            total += priority
        print(total)