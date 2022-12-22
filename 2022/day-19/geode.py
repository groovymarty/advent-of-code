import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

resource_names = ["ore", "clay", "obsidian", "geode"]
resource_map = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}
blueprints = []

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


def minute(time_left):
    return 25 - time_left


def can_make_robots(blueprint, resources):
    return tuple(i for i in range(0, 4) if all(cost <= have for cost, have in zip(blueprint[i], resources)))


def get_names(these):
    return ", ".join(resource_names[this] for this in these)


def make_resources(blueprint, resources_wanted, state, path):
    resources, robots, time_left = state
    path += f"make_resources{resources_wanted}: "
    # make any required robots
    for i in range(0, 4):
        if resources_wanted[i] != 0 and robots[i] == 0:
            state = make_robot(blueprint, i, state, path)
            if state is None:
                return None
            resources, robots, time_left = state
    # wait for resources to accumulate
    while any(have < wanted for have, wanted in zip(resources, resources_wanted)):
        if time_left <= 0:
            return (resources, robots, time_left) if 999 in resources_wanted else None
        # what robots can I make with total resources on hand?
        can_make = can_make_robots(blueprint, resources)
        print(f"  min {minute(time_left)}: {path}{resources} {robots} can make {get_names(can_make)}")
        # degree of freedom is here.. need to search for best answer...
        make_me = None
        if GEODE in can_make:
            make_me = GEODE
        elif OBSIDIAN in can_make and robots[OBSIDIAN] < 2:
            make_me = OBSIDIAN
        elif CLAY in can_make and robots[CLAY] < (3 if robots[OBSIDIAN] == 0 else 4):
            make_me = CLAY
        if make_me:
            state = (resources, robots, time_left)
            state = make_robot(blueprint, make_me, state, path)
            if state is None:
                raise IndexError("Failed to make robot even though required resources were available!")
            resources, robots, time_left = state
        else:
            # let the robots work for a minute
            resources = tuple(have + more for have, more in zip(resources, robots))
            time_left -= 1
    return resources, robots, time_left


def make_robot(blueprint, robot_wanted, state, path):
    path += f"make_robot({robot_wanted}): "
    robot_cost = blueprint[robot_wanted]
    state = make_resources(blueprint, robot_cost, state, path)
    if state is None:
        return None
    resources, robots, time_left = state
    if time_left <= 0:
        return None
    print(f"  min {minute(time_left)}: {path}{resources} {robots} making {resource_names[robot_wanted]}")
    resources = tuple(have - cost + more for have, cost, more in zip(resources, robot_cost, robots))
    robots = list(robots)
    robots[robot_wanted] += 1
    time_left -= 1
    return resources, robots, time_left


initial_state = ([0, 0, 0, 0], [1, 0, 0, 0], 24)

for i, blueprint in enumerate(blueprints):
    state = make_resources(blueprint, (0, 0, 0, 999), initial_state, "")
    if state is None:
        print(f"{i + 1}: None")
    else:
        resources, robots, time_left = state
        print(f"{i + 1}: resources: {resources}, robots: {robots}, time left: {time_left}")
