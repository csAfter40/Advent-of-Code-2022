points = {
    'A X': 3,
    'A Y': 4,
    'A Z': 8,
    'B X': 1,
    'B Y': 5,
    'B Z': 9,
    'C X': 2,
    'C Y': 6,
    'C Z': 7,
}

with open('2/rock_paper_scissors.txt') as f:
    lines = f.readlines()
    total = 0
    for line in lines:
        total += points[line.strip()]
    print(total)