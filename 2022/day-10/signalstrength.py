x = 1
cycle = 1
sum_ = 0


def sim_cycle():
    global x, cycle, sum_
    if cycle in [20, 60, 100, 140, 180, 220]:
        sum_ += cycle * x
    cycle += 1


with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        parts = line.split()
        if parts[0] == "addx":
            sim_cycle()
            sim_cycle()
            x += int(parts[1])
        elif parts[0] == "noop":
            sim_cycle()
        else:
            print(f"unrecognized instruction: {line}")

print(sum_)
