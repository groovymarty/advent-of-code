import re


# lookup valve by name
valve_name_map = {}

# all valves
valves = []

# working valves
working_valves = []


class Valve:
    def __init__(self, name, flow_rate, tunnels):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels
        self.neighbors = None
        self.visited = False
        self.cost = None
        self.transit_costs = None
        valve_name_map[name] = self

    def search_transit_cost(self, cost):
        if not self.visited or cost < self.cost:
            self.visited = True
            self.cost = cost
            for neighbor in self.neighbors:
                neighbor.search_transit_cost(cost + 1)


def clear_all_visited():
    for valve in valves:
        valve.visited = False


with open('input.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        mr = re.match(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)', line)
        if not mr:
            raise SyntaxError(f"Bad input: {line}")
        name = mr.group(1)
        flow_rate = int(mr.group(2))
        tunnels = [tunnel.strip() for tunnel in mr.group(3).split(",")]
        valves.append(Valve(name, flow_rate, tunnels))

# valve AA is puzzle starting point
puzzle_start = valve_name_map["AA"]

# build list of neighbors for each valve
for valve in valves:
    valve.neighbors = [valve_name_map[tunnel] for tunnel in valve.tunnels]

print("Neighbors:")
for valve in valves:
    print(f"{valve.name}: {[neighbor.name for neighbor in valve.neighbors]}")

# find working valves
working_valves = [valve for valve in valves if valve.flow_rate != 0]

# compute transit cost from each working value to every other working valve
# also include the puzzle starting point because we need transit costs from there to all working valves
for start_valve in [puzzle_start] + working_valves:
    clear_all_visited()
    start_valve.search_transit_cost(0)
    start_valve.transit_costs = [valve.cost for valve in working_valves]

print("Transit costs:")
for valve in [puzzle_start] + working_valves:
    print(f"{valve.name}: {valve.transit_costs}")

# search for best solution
stack = []
my_pos = puzzle_start
my_delay = 0
my_index = 0
el_pos = puzzle_start
el_delay = 0
el_index = 0
time_left = 26
score_so_far = 0
best_score = 0
visited = 0
path = ""


def is_visited(index):
    return (visited >> index) & 1


def set_visited(index):
    global visited
    visited |= (1 << index)


while True:
    found_move = False
    # do I have a move?
    if my_delay == 0:
        while my_index < len(working_valves):
            if not is_visited(my_index) and my_pos.transit_costs[my_index] + 1 <= time_left:
                # push stack
                stack.append((my_pos, my_delay, my_index + 1, el_pos, el_delay, el_index,
                              time_left, score_so_far, visited, path))
                # my move
                my_delay = my_pos.transit_costs[my_index] + 1
                my_pos = working_valves[my_index]
                set_visited(my_index)
                my_index = 0
                score_so_far += (time_left - my_delay) * my_pos.flow_rate
                best_score = max(best_score, score_so_far)
                path += f"me:{my_pos.name} "
                found_move = True
                break
            else:
                my_index += 1
    # does elephant have a move?
    if el_delay == 0:
        while el_index < len(working_valves):
            if not is_visited(el_index) and el_pos.transit_costs[el_index] + 1 <= time_left:
                # push stack
                stack.append((my_pos, my_delay, my_index, el_pos, el_delay, el_index + 1,
                              time_left, score_so_far, visited, path))
                # elephant's move
                el_delay = el_pos.transit_costs[el_index] + 1
                el_pos = working_valves[el_index]
                set_visited(el_index)
                el_index = 0
                score_so_far += (time_left - el_delay) * el_pos.flow_rate
                best_score = max(best_score, score_so_far)
                path += f"el:{el_pos.name} "
                found_move = True
                break
            else:
                el_index += 1
    if found_move:
        # minute = 27 - time_left
        # print(minute, path)
        pass
    else:
        # advance time
        t = min(my_delay, el_delay)
        if t > 0:
            my_delay -= t
            el_delay -= t
            time_left -= t
        elif len(stack) > 0:
            # pop stack
            my_pos, my_delay, my_index, el_pos, el_delay, el_index, time_left,\
                score_so_far, visited, path = stack.pop()
            # print("popped to minute", 27 - time_left)
            if len(stack) < 3:
                minute = 27 - time_left
                print(minute, path)
        else:
            break

print(best_score)
