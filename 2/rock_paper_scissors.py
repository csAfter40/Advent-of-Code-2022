points = {
    'A X': 4,
    'A Y': 8,
    'A Z': 3,
    'B X': 1,
    'B Y': 5,
    'B Z': 9,
    'C X': 7,
    'C Y': 2,
    'C Z': 6,
}

with open('2/rock_paper_scissors.txt') as f:
    lines = f.readlines()
    total = 0
    for line in lines:
        total += points[line.strip()]
    print(total)