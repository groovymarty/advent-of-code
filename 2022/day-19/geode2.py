import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

resource_names = ["ore", "clay", "obsidian", "geode"]
resource_map = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}
blueprints = []
blueprint = None
obsidian_needed = 0
time_to_play = 32
max_geode_time_left = 0
projected_resource = [0] + [t for t in range(0, time_to_play)]
for i in range(1, len(projected_resource)):
    projected_resource[i] += projected_resource[i-1]
print(projected_resource)

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

    def evaluate(self):
        return self.resources[GEODE]

    def get_minute(self):
        return time_to_play - self.time_left + 1

    def projected_obsidian(self, t):
        t = max(t, 0)
        return self.resources[OBSIDIAN] + (self.robots[OBSIDIAN] * t) + projected_resource[t]

    def is_possible_to_make_geode_robot(self):
        resources = self.resources
        robots = self.robots
        for t in range(self.time_left, 0, -1):
            # for each robot type, see if we have the resources to make a robot of that type
            can_make_robot = tuple(all(have >= need for have, need in zip(resources, cost)) for cost in blueprint)
            # return true if we can a geode robot
            if can_make_robot[GEODE]:
                return True
            # make new resources with existing robots
            resources = tuple(have + more for have, more in zip(resources, robots))
            # make new robots (without consuming any resources)
            robots = tuple(n + 1 if can_make else 0 for n, can_make in zip(robots, can_make_robot))
        return False


def play(state):
    global max_geode_time_left
    best_result = state
    best_score = -1
    # must have at least 2 minutes left or no point making any robots
    # also no point in making robots if it's impossible to make a geode robot in the time remaining
    if state.time_left > 1 and state.is_possible_to_make_geode_robot():
        # print(f"{state.get_minute()}: {state.path}")
        # try making each type of robot, higher-value robots first
        for robot in range(GEODE, -1, -1):
            if state.can_make_robot(robot):
                # keep track of earliest point in time when a geode robot was made
                if robot == GEODE and state.time_left >= max_geode_time_left:
                    max_geode_time_left = state.time_left
                    print(f"{state.get_minute()}: {state.path} making geode robot")
                try_state = State(state)
                try_state.make_robot(robot)
                result = play(try_state)
                result_score = result.evaluate()
                if result_score > best_score:
                    best_score = result_score
                    best_result = result

    # also try letting time pass without making a robot
    if state.time_left > 0:
        try_state = State(state)
        try_state.pass_time()
        result = play(try_state)
        result_score = result.evaluate()
        if result_score > best_score:
            best_result = result
    return best_result


product = 1
for i, blueprint in enumerate(blueprints[0:3]):
    print(f"doing blueprint {i+1}:")
    obsidian_needed = blueprint[GEODE][OBSIDIAN]
    state = State()
    state.set_initial_state()
    max_geode_time_left = 0
    result = play(state)
    print("got", result.evaluate())
    product *= result.evaluate()

print(product)
