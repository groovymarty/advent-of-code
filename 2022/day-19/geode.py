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
time_to_play = 24
much_time_left = 0
max_geode_time_left = 0
projected_resource = [t for t in range(0, time_to_play)]
for t in range(1, time_to_play):
    projected_resource[t] += projected_resource[t-1]
print(projected_resource)

with open('input.txt') as f:
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

    def projected_obsidian(self):
        return 999
        t = max(self.time_left - 1, 0)
        return self.resources[OBSIDIAN] + (self.robots[OBSIDIAN] * t) + projected_resource[t]


def play(state):
    global max_geode_time_left, max_obsidian_time_left
    best_result = state
    if state.time_left > 1 and \
        (state.robots[GEODE] or \
            (state.time_left >= max_geode_time_left)):
        #print(f"{state.get_minute()}: {state.path}")
        best_score = -1
        # try making each type of robot, higher-value robots first
        # only make ore robots early in the game
        for robot in range(GEODE, -1, -1):
            if state.robots[robot] < 10 and state.can_make_robot(robot):
                # keep track of earliest point in time when a geode robot was made
                if robot == GEODE and state.time_left > max_geode_time_left:
                    max_geode_time_left = state.time_left
                    print("made geode robot", max_geode_time_left)
                try_state = State(state)
                try_state.make_robot(robot)
                result = play(try_state)
                if robot == GEODE:
                    # no way to improve on making a geode robot when possible
                    return result
                result_score = result.evaluate()
                if result_score > best_score:
                    best_score = result_score
                    best_result = result
        # also try letting time pass without making a robot (only early in game or unable to make any robots)
        if best_score == -1 or state.time_left >= much_time_left:
            try_state = State(state)
            try_state.pass_time()
            result = play(try_state)
            result_score = result.evaluate()
            if result_score > best_score:
                best_result = result
    elif state.time_left == 1:
        # no point making any robots in last minute
        best_result.pass_time()
    return best_result


quality_total = 0
for i, blueprint in enumerate(blueprints):
    print(f"doing blueprint {i+1}:")
    obsidian_needed = blueprint[GEODE][OBSIDIAN]
    state = State()
    state.set_initial_state()
    max_geode_time_left = 0
    result = play(state)
    print("got", result.evaluate())
    quality_total += result.evaluate() * (i + 1)

print(quality_total)
