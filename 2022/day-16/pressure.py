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

    def search_best_score(self, time_left, score_so_far, state):
        result = score_so_far
        if time_left > 0 and not self.visited:
            self.visited = True
            state += self.name + ","
            # print(state, score_so_far)
            if self.flow_rate != 0:
                time_left -= 1
                score_so_far += self.flow_rate * time_left
                result = score_so_far
            for valve, transit_cost in zip(working_valves, self.transit_costs):
                if transit_cost != 0:
                    result = max(result, valve.search_best_score(time_left - transit_cost, score_so_far, state))
            self.visited = False
        return result


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
clear_all_visited()
result = puzzle_start.search_best_score(30, 0, "")
print(result)
