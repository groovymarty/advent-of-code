import re


def manhattan_distance(pt1, pt2):
    return abs(pt2[0] - pt1[0]) + abs(pt2[1] - pt1[1])


class Sensor:
    def __init__(self, pos, closest_beacon):
        self.pos = pos
        self.closest_beacon = closest_beacon
        self.closest_dist = manhattan_distance(pos, closest_beacon)


sensors = []

with open('input.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        mr = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
        if not mr:
            raise ValueError(f"Bad input: {line}")
        x = int(mr.group(1))
        y = int(mr.group(2))
        closest_x = int(mr.group(3))
        closest_y = int(mr.group(4))
        sensors.append(Sensor((x, y), (closest_x, closest_y)))


max_closest_dist = max([sensor.closest_dist for sensor in sensors])
min_pos_x = min([sensor.pos[0] for sensor in sensors])
max_pos_x = max([sensor.pos[0] for sensor in sensors])
print("max_closest_dist", max_closest_dist)
print("max_pos_x", max_pos_x)
print("min_pos_x", min_pos_x)

y_of_interest = 2000000

occupied_x = [sensor.pos[0] for sensor in sensors if sensor.pos[1] == y_of_interest]
occupied_x += [sensor.closest_beacon[0] for sensor in sensors if sensor.closest_beacon[1] == y_of_interest]
print("occupied_x", occupied_x)

n = 0
for x in range(min_pos_x - max_closest_dist - 10, max_pos_x + max_closest_dist + 10):
    if x % 1000000 == 0:
        print(f"at x={x}, n={n}")
    if x in occupied_x:
        continue
    for sensor in sensors:
        if manhattan_distance((x, y_of_interest), sensor.pos) <= sensor.closest_dist:
            n += 1
            break
print(n)
