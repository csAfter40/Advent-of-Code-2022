from typing import Tuple

def get_signal(path:str) -> str:
    """
    Given path of a file, reads and returns string in the first line of the text file.
    """
    with open(path) as f:
        return f.readlines()[0].rstrip("\n")

def find_marker(signal:str, length:int) -> Tuple[str, int]:
    """
    Given a string of signal and length, returns marker string and it's position in signal.
    """
    marker = ""
    marker_position = 0
    for i in range(len(signal) - length + 1):
        if len(set(signal[i:i+length])) == length:
            marker = signal[i:i+length]
            marker_position = i+length
            break
    return marker, marker_position

def print_marker(marker:str, marker_position:int) -> None:
    """
    Given a marker string and position, prints formatted info on the console.
    """
    print(f"marker is '{marker}' and first marker appears after character { marker_position}")

if __name__ == "__main__":
    signal = get_signal("6/tuning_trouble.txt")
    # Problem part1
    print_marker(*find_marker(signal, 4))
    # Problem part2
    print_marker(*find_marker(signal, 14))
    