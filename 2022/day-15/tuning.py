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

search_limit = 4000000
for y in range(0, search_limit):
    if y % 100000 == 0:
        print("y", y)
    # for each sensor, figure out range of x coordinates that are as close as, or closer, than that sensor's
    # detected beacon
    # this is called the skip list because the distress beacon cannot be in any of these ranges,
    # or else it would have been detected
    skip_list = []
    for sensor in sensors:
        delta_y = abs(y - sensor.pos[1])
        delta_x = sensor.closest_dist - delta_y
        if delta_x >= 0:
            skip_list.append((max(0, sensor.pos[0] - delta_x), min(sensor.pos[0] + delta_x + 1, search_limit)))
    # sort the skip list by starting x value
    skip_list.sort(key=lambda item: item[0])
    # now take the full range, 0 to 4000000, and knock out the skip list ranges
    # the result is the scan list, that is, the list of candidate ranges where the distress beacon might be
    scan_list = []
    start_x = 0
    for skip in skip_list:
        if start_x < skip[0]:
            scan_list.append((start_x, skip[0]))
        if start_x < skip[1]:
            start_x = skip[1]
    if start_x < search_limit:
        scan_list.append((start_x, search_limit))
    # nonempty scan list?
    if len(scan_list) > 0:
        print("found", scan_list)
        # according to the problem statement, there should be exactly one possible location for the distress beacon
        if len(scan_list) != 1:
            print("scan list is too long")
        elif scan_list[0][1] - scan_list[0][0] != 1:
            print("scan range is not exactly one position")
        else:
            tuning = (scan_list[0][0] * 4000000) + y
            print("tuning", tuning)
        break
