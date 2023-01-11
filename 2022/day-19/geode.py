import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

resource_names = ["ore", "clay", "obsidian", "geode"]
resource_map = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}
blueprints = []
blueprint = None
blueprint_num = 0
obsidian_needed = 0
# this version gets the correct answer for the part one, but not for part two
# you can run this version for part two using the commented out values below, but it won't get the right answer
# I think both trick #1 and #2 are not applicable for part 2 (32 rounds instead of 24), but if you take them
# out the exhaustive search takes too long.  Will try another approach in geode2.
time_to_play = 24  # 32
max_blueprints = 999  # 3
max_geode_time_left = 0

with open('example.txt') as f:
    lines = f.readlines()
    for line in lines:
        phrases = line.strip().split(".")
        blueprint = [[0, 0, 0, 0] for i in range(0, 4)]
        blueprints.append(blueprint)
        for phrase in phrases:
            if phrase == "":
                continue
            mr = re.search(r'Each (\w+) robot costs (.*)', phrase)
            if not mr:
                raise SyntaxError(f"invalid phrase: {phrase}")
            what = mr.group(1)
            if what not in resource_map:
                raise ValueError(f"no such robot: {what}")
            robot = resource_map[what]
            costs = mr.group(2).split(" and ")
            for cost in costs:
                mr = re.search(r'(\d+) (\w*)', cost)
                if not mr:
                    raise SyntaxError(f"invalid cost: {cost}")
                num = int(mr.group(1))
                what = mr.group(2)
                if what not in resource_map:
                    raise ValueError(f"no such resource: {what}")
                resource = resource_map[what]
                blueprint[robot][resource] = num

for i, blueprint in enumerate(blueprints):
    print(f"{i + 1}: {blueprint}")


def get_names(these):
    return ", ".join(resource_names[this] for this in these)


class State:
    def __init__(self, other=None):
        if other:
            self.resources = other.resources
            self.robots = other.robots
            self.path = other.path
            self.time_left = other.time_left
        else:
            self.resources = None
            self.robots = None
            self.path = ""
            self.time_left = 0

    def set_initial_state(self):
        self.resources = (0, 0, 0, 0)
        self.robots = (1, 0, 0, 0)
        self.path = ""
        self.time_left = time_to_play

    def can_make_robot(self, robot):
        return all(have >= need for have, need in zip(self.resources, blueprint[robot]))

    def make_robot(self, robot):
        self.resources = tuple(have - cost + more for have, cost, more in zip(self.resources, blueprint[robot], self.robots))
        my_robots = list(self.robots)
        my_robots[robot] += 1
        self.robots = tuple(my_robots)
        self.path += f"{resource_names[robot]},"
        self.time_left -= 1

    def pass_time(self):
        self.resources = tuple(have + more for have, more in zip(self.resources, self.robots))
        self.path += ","
        self.time_left -= 1

    def get_minute(self):
        return time_to_play - self.time_left + 1


def play(state):
    global max_geode_time_left
    num_geodes_max = 0
    # must have at least 2 minutes left or no point making any robots
    # also don't take longer to make first geode robot than best time found so far (trick #1)
    if state.time_left > 1 and \
            (state.robots[GEODE] or state.time_left >= max_geode_time_left):
        #print(f"{state.get_minute()}: {state.path}")
        # try making each type of robot, higher-value robots first
        any_robot = False
        for robot in range(GEODE, -1, -1):
            if state.can_make_robot(robot):
                any_robot = True
                # keep track of earliest point in time when a geode robot was made
                if robot == GEODE and state.time_left >= max_geode_time_left:
                    max_geode_time_left = state.time_left
                    print(f"[{blueprint_num}] {state.get_minute()}: {state.path} making geode robot")
                try_state = State(state)
                try_state.make_robot(robot)
                num_geodes_max = max(num_geodes_max, play(try_state))
                # if geode robot just made, don't consider other possibilities (trick #2)
                if robot == GEODE:
                    return num_geodes_max
        # also try letting time pass without making a robot
        if not any_robot:
            try_state = State(state)
            try_state.pass_time()
            num_geodes_max = max(num_geodes_max, play(try_state))
        return num_geodes_max
    else:
        # not gonna bother making any more robots, run out the clock with the existing robots
        return state.resources[GEODE] + state.robots[GEODE] * state.time_left


num_geodes_results = []
max_geode_time_lefts = []
quality_total = 0
product = 1
for i, blueprint in enumerate(blueprints[0: max_blueprints]):
    blueprint_num = i + 1
    print(f"doing blueprint {blueprint_num}:")
    state = State()
    state.set_initial_state()
    max_geode_time_left = 0
    num_geodes = play(state)
    num_geodes_results.append(num_geodes)
    max_geode_time_lefts.append(max_geode_time_left)
    print("got", num_geodes)
    quality_total += num_geodes * blueprint_num
    product *= num_geodes

print("geodes", num_geodes_results)
print("m_g_t_l", max_geode_time_lefts)
print("quality", quality_total)
print("product", product)
