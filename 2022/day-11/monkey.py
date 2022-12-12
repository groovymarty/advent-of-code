import re


TURN = 3   # log messages for each monkey's turn
ROUND = 2  # log messages for each round
TOP = 1    # top-level log messages
log_level = TOP


def log(level, msg):
    if level <= log_level:
        print(msg)


class Monkey:
    def __init__(self, num):
        self.items = []
        self.num = num
        self.operation = None
        self.test = None
        self.throw_to_if_true = None
        self.throw_to_if_false = None
        self.items_inspected = 0

    def do_turn(self):
        log(TURN, f"Monkey {self.num}:")
        items = self.items
        self.items = []
        for item in items:
            self.items_inspected += 1
            log(TURN, f"  Monkey inspects item with worry level of {item}")
            item = self.operation(item)
            log(TURN, f"  Applying operation changes worry level to {item}")
            item //= 3
            log(TURN, f"  Monkey gets bored with item. Worry level is divided by 3 to {item}")
            if monkey.test(item):
                log(TURN, f"  Test is true. Item with worry level {item} is thrown to monkey {self.throw_to_if_true}")
                monkeys[self.throw_to_if_true].items.append(item)
            else:
                log(TURN, f"  Test is false. Item with worry level {item} is thrown to monkey {self.throw_to_if_false}")
                monkeys[self.throw_to_if_false].items.append(item)


# array of monkeys
monkeys = []

# iterator for input lines, used by parsing functions
lines_iter = None

# one-line buffer for parsing functions
line_buf = None


def print_monkeys(level):
    if level <= log_level:
        for monkey in monkeys:
            print(f"Monkey {monkey.num}: {', '.join([str(item) for item in monkey.items])}")


# get next line
# return None if no more lines
def get_line():
    global line_buf, lines_iter
    if line_buf is not None:
        line = line_buf
        line_buf = None
    else:
        try:
            line = next(lines_iter)
        except StopIteration:
            line = None
    return line


# give back line so it can be gotten again
# if line is None, clears buffer
def unget_line(line):
    global line_buf
    line_buf = line


# parse functions take current line, possibly consume more lines,
# and give back the last line read if they can't use it
def parse_starting_items(line, monkey):
    mr = re.match(r'Starting items: ([\d,\s]*)', line)
    if not mr:
        raise SyntaxError(f"Bad starting items: {line}")
    parts = mr.group(1).split(",")
    monkey.items = [int(part.strip()) for part in parts]


def parse_operation(line, monkey):
    mr = re.match(r'Operation: new = old ([+*]) ([old\d]+)', line)
    if not mr:
        raise SyntaxError(f"Bad operation: {line}")
    op = mr.group(1)
    if op == "*" and mr.group(2) == "old":
        monkey.operation = lambda x: x * x
    else:
        val = int(mr.group(2))
        if op == "+":
            monkey.operation = lambda x: x + val
        else:
            monkey.operation = lambda x: x * val


def parse_test(line, monkey):
    mr = re.match(r'Test: divisible by (\d+)', line)
    if not mr:
        raise SyntaxError(f"Bad test: {line}")
    val = int(mr.group(1))
    monkey.test = lambda x: x % val == 0
    while True:
        line = get_line()
        if line is None:
            break
        elif line == "":
            continue
        else:
            mr = re.match(r'If (\w+): throw to monkey (\d+)', line)
            if not mr:
                break
            cond = mr.group(1)
            to_num = int(mr.group(2))
            if cond == "true":
                monkey.throw_to_if_true = to_num
            elif cond == "false":
                monkey.throw_to_if_false = to_num
            else:
                raise SyntaxError(f"Bad if condition: {line}")
    unget_line(line)


def parse_monkey(line):
    mr = re.match(r'Monkey (\d+):', line)
    if not mr:
        raise SyntaxError(f"Bad monkey: {line}")
    num = int(mr.group(1))
    monkey = Monkey(num)
    while True:
        line = get_line()
        if line is None:
            break
        elif line == "":
            continue
        elif line.startswith("Starting items"):
            parse_starting_items(line, monkey)
        elif line.startswith("Operation"):
            parse_operation(line, monkey)
        elif line.startswith("Test"):
            parse_test(line, monkey)
        else:
            break
    unget_line(line)
    return monkey


with open('input.txt') as f:
    lines = f.readlines()

    # remove leading/trailing whitespace
    # this throws away the indentation, which you could also use in your parser (like Python)
    lines = [line.strip() for line in lines]
    lines_iter = iter(lines)
    monkey = None
    while True:
        line = get_line()
        if line is None:
            break
        elif line == "":
            continue
        elif line.startswith("Monkey"):
            monkey = parse_monkey(line)
            if monkey.num != len(monkeys):
                print(monkey.num, len(monkeys))
                raise ValueError(f"Monkey {monkey.num} out of order")
            monkeys.append(monkey)
            log(TOP, f"Monkey {monkey.num} added")
        else:
            raise SyntaxError(f"Unexpected line: {line}")

log(TOP, "Initial state:")
print_monkeys(TOP)
for round in range(0, 20):
    for monkey in monkeys:
        monkey.do_turn()
    log(ROUND, f"After round {round+1}, the monkeys are holding items with these worry levels:")
    print_monkeys(ROUND)

for monkey in monkeys:
    log(TOP, f"Monkey {monkey.num} inspected items {monkey.items_inspected} times.")

counts = [monkey.items_inspected for monkey in monkeys]
sorted_counts = sorted(counts, reverse=True)
print(sorted_counts[0] * sorted_counts[1])
