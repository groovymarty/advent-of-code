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
guess_vector = 0
guess_vector_length = 18
guess_bits_left = 0


def set_initial_state():
    global resources, robots, time_left, guesses
    resources = (0, 0, 0, 0)
    robots = [1, 0, 0, 0]
    time_left = time_to_play


def get_minute():
    return time_to_play - time_left + 1


class TimeIsUp(Exception):
    pass


class OutOfGuesses(Exception):
    pass


def make_resources(resources_wanted, path):
    global resources, robots, time_left, guess_vector, guess_bits_left
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
        # don't bother making low-value robots at end of game
        can_make = tuple(i for i in range(0, 4) if all(cost <= have for cost, have in zip(blueprint[i], resources)) and (time_left > [4, 2, 0, 0][i]))
        # print(f"  min {get_minute()}: {path}{resources} {robots} can make {get_names(can_make)}")
        # always make geode robot if possible
        make_me = None
        if GEODE in can_make:
            make_me = GEODE
        elif len(can_make) > 0:
            # always make robot for which there is great need
            great_need = sorted((robot for robot in can_make if resources_wanted[robot] > robots[robot] * 5), reverse=True)
            if len(great_need) > 0:
                # print(f"  min {get_minute()}: {path}{resources} {robots} great need {get_names(great_need)}")
                make_me = great_need[0]
            else:
                if len(can_make) == 1:
                    # consume one guess bit
                    guess_mask = 1
                    guess_shift = 1
                else:
                    # consume two guess bits
                    guess_mask = 3
                    guess_shift = 2
                # print(f"  min {get_minute()}: {path}{resources} {robots} consuming {guess_shift} of {guess_bits_left}")
                if guess_shift > guess_bits_left:
                    raise OutOfGuesses
                guess = guess_vector & guess_mask
                guess_vector >>= guess_shift
                guess_bits_left -= guess_shift
                if guess < len(can_make):
                    make_me = can_make[guess]
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
    # print(f"  min {get_minute()}: {path}{resources} {robots} making {resource_names[robot_wanted]}")
    resources = tuple(have - cost + more for have, cost, more in zip(resources, robot_cost, robots))
    robots[robot_wanted] += 1
    time_left -= 1


for i, blueprint in enumerate(blueprints):
    max_geodes = 0
    for guess_vector in range(0, 1 << guess_vector_length):
        #if guess_vector & 0x3ff == 0:
        #    print(guess_vector >> 10)
        guess_bits_left = guess_vector_length
        set_initial_state()
        try:
            make_resources((0, 0, 0, 999), "")
        except TimeIsUp:
            pass
        max_geodes = max(max_geodes, resources[GEODE])
    print(f"{i+1}: {max_geodes}")
