import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

resource_names = {"ore": ORE, "clay": CLAY, "obsidian": OBSIDIAN, "geode": GEODE}
blueprints = []

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
            if what not in resource_names:
                raise ValueError(f"no such robot: {what}")
            robot = resource_names[what]
            costs = mr.group(2).split(" and ")
            for cost in costs:
                mr = re.search(r'(\d+) (\w*)', cost)
                if not mr:
                    raise SyntaxError(f"invalid cost: {cost}")
                num = int(mr.group(1))
                what = mr.group(2)
                if what not in resource_names:
                    raise ValueError(f"no such resource: {what}")
                resource = resource_names[what]
                blueprint[robot][resource] = num

for i, blueprint in enumerate(blueprints):
    print(f"{i + 1}: {blueprint}")


def can_pay(resources, prices):
    return all(have >= price for have, price in zip(resources, prices))


def withdraw(resources, amounts):
    return tuple(have - amount for have, amount in zip(resources, amounts))


def deposit(resources, amounts):
    return tuple(have + amount for have, amount in zip(resources, amounts))


def make_resource(blueprint, resource_wanted, amount_wanted, state):
    resources, robots, time_left = state
    while resources[resource_wanted] < amount_wanted and time_left > 0:
        if robots[resource_wanted] == 0:
            state = make_robot(blueprint, resource_wanted, state)
            if state is None:
                break
            resources, robots, time_left = state
        else:
            # let one minute pass by...
            resources = deposit(resources, robots)
            time_left -= 1
            state = (resources, robots, time_left)
    return state


def make_robot(blueprint, robot_wanted, state):
    resources, robots, time_left = state
    for i in range(0, 4):
        if resources[i] < blueprint[robot_wanted][i]:
            state = make_resource(blueprint, i, blueprint[robot_wanted][i] - resources[i], state)
            if state is None:
                break
            resources, robots, time_left = state
    if state is not None and time_left > 0:
        resources = withdraw(resources, blueprint[robot_wanted])
        robots = list(robots)
        robots[robot_wanted] += 1
        time_left -= 1
        state = (resources, robots, time_left)
    return state


initial_state = ([0, 0, 0, 0], [1, 0, 0, 0], 24)

for i, blueprint in enumerate(blueprints):
    resources, robots, time_left = make_resource(blueprint, GEODE, 1, initial_state)
    print(f"{i + 1}: resources: {resources}, robots: {robots}, time left: {time_left}")
