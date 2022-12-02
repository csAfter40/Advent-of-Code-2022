with open('calories.txt') as f:
    lines = f.readlines()
    best = 0
    current_total = 0
    for line in lines:
        if line == '\n':
            if current_total > best:
                best = current_total
            current_total = 0
            continue
        calory = int(line)
        current_total += calory
    print(best)