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

if __name__ == '__main__':
    with open('3/rucksack.txt') as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            item = get_share_item(line)
            priority = get_priority(item)
            total += priority
        print(total)