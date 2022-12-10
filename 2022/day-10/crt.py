x = 1
cycle = 1
screen = ""


def sim_cycle():
    global x, cycle, screen
    pos = (cycle - 1) % 40
    screen += "#" if x - 1 <= pos <= x + 1 else "."
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

for i in range(0, 240, 40):
    print(screen[i: i+40])
