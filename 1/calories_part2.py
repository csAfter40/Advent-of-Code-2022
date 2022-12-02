with open('1/calories.txt') as f:
    lines = f.readlines()
    bests = [0]
    current_total = 0
    for line in lines:
        if line == '\n':
            for i, item in enumerate(bests[:3]):
                if current_total >= item:
                    bests.insert(i, current_total)
                    break
            current_total = 0
            continue
        calory = int(line)
        current_total += calory
    print(sum(bests[:3]))