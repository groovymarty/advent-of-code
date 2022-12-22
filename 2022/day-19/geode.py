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


def get_names(these):
    return ", ".join(resource_names[this] for this in these)


blueprint = None
resources = None
robots = None
time_to_play = 24
time_left = 0


def set_initial_state():
    global resources, robots, time_left
    resources = (0, 0, 0, 0)
    robots = [1, 0, 0, 0]
    time_left = time_to_play


def get_minute():
    return time_to_play - time_left + 1


class TimeIsUp(Exception):
    pass


def make_resources(resources_wanted, path):
    global resources, robots, time_left
    path += f"make_resources{resources_wanted}: "
    # make any required robots
    for i in range(0, 4):
        if resources_wanted[i] != 0 and robots[i] == 0:
            make_robot(i, path)
    # wait for resources to accumulate
    while any(have < wanted for have, wanted in zip(resources, resources_wanted)):
        if time_left <= 0:
            raise TimeIsUp
        # what additional robots can I make with resources on hand?
        can_make = tuple(i for i in range(0, 4) if all(cost <= have for cost, have in zip(blueprint[i], resources)))
        print(f"  min {get_minute()}: {path}{resources} {robots} can make {get_names(can_make)}")
        # degree of freedom is here.. need to search for best answer...
        make_me = None
        if GEODE in can_make:
            make_me = GEODE
        elif OBSIDIAN in can_make and robots[OBSIDIAN] < 2:
            make_me = OBSIDIAN
        elif CLAY in can_make and robots[CLAY] < (3 if robots[OBSIDIAN] == 0 else 4):
            make_me = CLAY
        if make_me:
            make_robot(make_me, path)
        else:
            # let the robots work for a minute
            resources = tuple(have + more for have, more in zip(resources, robots))
            time_left -= 1


def make_robot(robot_wanted, path):
    global resources, robots, time_left
    path += f"make_robot({robot_wanted}): "
    robot_cost = blueprint[robot_wanted]
    make_resources(robot_cost, path)
    if time_left <= 0:
        raise TimeIsUp
    print(f"  min {get_minute()}: {path}{resources} {robots} making {resource_names[robot_wanted]}")
    resources = tuple(have - cost + more for have, cost, more in zip(resources, robot_cost, robots))
    robots[robot_wanted] += 1
    time_left -= 1


for i, blueprint in enumerate(blueprints):
    set_initial_state()
    try:
        make_resources((0, 0, 0, 999), "")
    except TimeIsUp:
        pass
    print(f"{i + 1}: resources: {resources}, robots: {robots}")
