from typing import List
from helpers import print_matrix

INITIAL_SIGNAL = 1
MAXIMUM_TRESHOLD = 220
CTR_SIZE = (6, 40)

def get_lines(path:str) -> List[str]:
    """
    Reads the file at given path and return cleaned lines as an array.
    """
    with open(path) as f:
        return [line.rstrip("\n") for line in f.readlines()]

def get_commands(path:str) -> List[List]:
    """
    Given a file path, returns list of commands.
    """
    lines = get_lines(path)
    return [line.split() for line in lines]

def execute_commands(commands:List[List]) -> List[int]:
    """
    Given a list of commnads, executes and records a list of signals for each 
    cycle. Returns the list of signals.
    """
    signal = INITIAL_SIGNAL
    signals = [signal]
    for command in commands:
        instruction = command[0]
        if instruction == "noop":
            signals.append(signal)
            continue
        elif instruction == "addx":
            signals.append(signal)
            signal += int(command[1])
            signals.append(signal)
    return signals

def get_multiplied_signals(signals:List[List]):
    """
    Given a list of signals and a limit treshold, calulates multiplied signals 
    for each treshold and returns a list of multiplied signals.
    """
    multiplied_signals = []
    tresholds = range(20, MAXIMUM_TRESHOLD+1, 40)
    for treshold in tresholds:
        multiplied_signal = signals[treshold-1]*treshold
        multiplied_signals.append(multiplied_signal)
    return multiplied_signals

def get_ctr() -> List[List]:
    """
    Creates and returns a list of lists representing pixels on a CTR where 
    blank pixels are represented by '.' and lit pixels are represented by '#'.
    In this case all pixels are blank initially.
    """
    return [['.' for pixel in range(CTR_SIZE[1])] for row in range(CTR_SIZE[0])]

def draw_on_ctr(ctr:List[List], signals:List[int]) -> List[List]:
    """
    Given a CTR and list of signals for each cycle, draws pixels on CTR and 
    returns final screen.
    """
    for j, row in enumerate(ctr):
        for i, value in enumerate(row):
            sprite = signals[i + 40*j]
            if i in range(sprite-1, sprite+2):
                ctr[j][i] = "#"
    return ctr

if __name__ == "__main__":
    commands = get_commands("10/cathode_ray.txt")
    signals = execute_commands(commands)
    # part 1
    multiplied_signals = get_multiplied_signals(signals)
    print(sum(multiplied_signals))
    # part 2
    ctr = get_ctr()
    screen = draw_on_ctr(ctr, signals)
    print_matrix(screen)

