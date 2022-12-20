with open('input.txt') as f:
    jets = f.readlines()[0].strip()

# a "cycle" is going through all combinations of jets and shapes.
# there are 5 shapes, but number of jets depends on your input (mine is 10091).
# so for my input, a cycle takes 5 * 10091 = 50455 loops.
# while the input pattern repeats every cycle, the tower is a form of memory so the overall pattern
# will probably not repeat every cycle.  we need to see how many cycles it takes before the "skyline"
# of the tower repeats itself (and therefore subsequent rocks will fall into the exact same pattern again).
# this is a "grand cycle" -- a total repetition of the whole state machine, including the tower "memory".
# each grand cycle leaves the tower in the same pattern (except it is some amount higher, H)
# divide a trillion by GC to get number of grand cycles, NGC, and remainder.
# answer is NGC * H plus run the remainder loops and add whatever more height they contribute

n_shapes = 5
n_cycle = len(jets) * n_shapes
print("n_cycle", n_cycle)

max_shape_h = 4
drop_h = 3
chamber_w = 7
y_dim = (n_cycle * max_shape_h) + drop_h + max_shape_h  # max possible height for one cycle
x_dim = 8
mem = bytearray((x_dim * y_dim * 2) // 8)  # enough room for 2 cycles
tower_h = 0


def get_bit(x, y):
    i = x + (y * x_dim)
    bit = 1 << (i % 8)
    return mem[i // 8] & bit


def is_occupied(x, y):
    return get_bit(x, y)


def is_vacant(x, y):
    return not get_bit(x, y)


def set_bit(x, y, val=1):
    i = x + (y * x_dim)
    bit = 1 << (i % 8)
    if val:
        mem[i // 8] |= bit
    else:
        mem[i // 8] &= ~bit


def set_occupied(x, y):
    set_bit(x, y)


class Shape:
    def __init__(self):
        # position of a shape is lower left corner of its bounding box
        self.kind = ""
        self.pos = (0, 0)
        self.h = 0

    def go_left(self):
        self.pos = (self.pos[0] - 1, self.pos[1])

    def go_right(self):
        self.pos = (self.pos[0] + 1, self.pos[1])

    def go_down(self):
        self.pos = (self.pos[0], self.pos[1] - 1)


class ShapeHLine(Shape):
    def __init__(self):
        self.kind = "HLine"
        self.h = 1

    def can_go_left(self):
        x, y = self.pos
        return x > 0 and \
            is_vacant(x - 1, y)

    def can_go_right(self):
        x, y = self.pos
        return x + 4 < chamber_w and \
            is_vacant(x + 4, y)

    def can_go_down(self):
        x, y = self.pos
        return y > 0 and \
            is_vacant(x, y - 1) and \
            is_vacant(x + 1, y - 1) and \
            is_vacant(x + 2, y - 1) and \
            is_vacant(x + 3, y - 1)

    def come_to_rest(self):
        x, y = self.pos
        set_occupied(x, y)
        set_occupied(x + 1, y)
        set_occupied(x + 2, y)
        set_occupied(x + 3, y)


class ShapePlus(Shape):
    def __init__(self):
        self.kind = "Plus"
        self.h = 3

    def can_go_left(self):
        x, y = self.pos
        return x > 0 and \
            is_vacant(x, y) and \
            is_vacant(x - 1, y + 1) and \
            is_vacant(x, y + 1)

    def can_go_right(self):
        x, y = self.pos
        return x + 3 < chamber_w and \
            is_vacant(x + 2, y) and \
            is_vacant(x + 3, y + 1) and \
            is_vacant(x + 2, y + 2)

    def can_go_down(self):
        x, y = self.pos
        return y > 0 and \
            is_vacant(x, y) and \
            is_vacant(x + 1, y - 1) and \
            is_vacant(x + 2, y)

    def come_to_rest(self):
        x, y = self.pos
        set_occupied(x + 1, y)
        set_occupied(x, y + 1)
        set_occupied(x + 1, y + 1)
        set_occupied(x + 2, y + 1)
        set_occupied(x + 1, y + 2)


class ShapeLRCorner(Shape):
    def __init__(self):
        self.kind = "LRCorner"
        self.h = 3

    def can_go_left(self):
        x, y = self.pos
        return x > 0 and \
            is_vacant(x - 1, y) and \
            is_vacant(x + 1, y + 1) and \
            is_vacant(x + 1, y + 2)

    def can_go_right(self):
        x, y = self.pos
        return x + 3 < chamber_w and \
            is_vacant(x + 3, y) and \
            is_vacant(x + 3, y + 1) and \
            is_vacant(x + 3, y + 2)

    def can_go_down(self):
        x, y = self.pos
        return y > 0 and \
            is_vacant(x, y - 1) and \
            is_vacant(x + 1, y - 1) and \
            is_vacant(x + 2, y - 1)

    def come_to_rest(self):
        x, y = self.pos
        set_occupied(x, y)
        set_occupied(x + 1, y)
        set_occupied(x + 2, y)
        set_occupied(x + 2, y + 1)
        set_occupied(x + 2, y + 2)


class ShapeVLine(Shape):
    def __init__(self):
        self.kind = "VLine"
        self.h = 4

    def can_go_left(self):
        x, y = self.pos
        return x > 0 and \
            is_vacant(x - 1, y) and \
            is_vacant(x - 1, y + 1) and \
            is_vacant(x - 1, y + 2) and \
            is_vacant(x - 1, y + 3)

    def can_go_right(self):
        x, y = self.pos
        return x + 1 < chamber_w and \
            is_vacant(x + 1, y) and \
            is_vacant(x + 1, y + 1) and \
            is_vacant(x + 1, y + 2) and \
            is_vacant(x + 1, y + 3)

    def can_go_down(self):
        x, y = self.pos
        return y > 0 and \
            is_vacant(x, y - 1)

    def come_to_rest(self):
        x, y = self.pos
        set_occupied(x, y)
        set_occupied(x, y + 1)
        set_occupied(x, y + 2)
        set_occupied(x, y + 3)


class ShapeBox(Shape):
    def __init__(self):
        self.kind = "Box"
        self.h = 2

    def can_go_left(self):
        x, y = self.pos
        return x > 0 and \
            is_vacant(x - 1, y) and \
            is_vacant(x - 1, y + 1)

    def can_go_right(self):
        x, y = self.pos
        return x + 2 < chamber_w and \
            is_vacant(x + 2, y) and \
            is_vacant(x + 2, y + 1)

    def can_go_down(self):
        x, y = self.pos
        return y > 0 and \
            is_vacant(x, y - 1) and \
            is_vacant(x + 1, y - 1)

    def come_to_rest(self):
        x, y = self.pos
        set_occupied(x, y)
        set_occupied(x + 1, y)
        set_occupied(x, y + 1)
        set_occupied(x + 1, y + 1)


def generate_shapes():
    while True:
        yield ShapeHLine()
        yield ShapePlus()
        yield ShapeLRCorner()
        yield ShapeVLine()
        yield ShapeBox()


def generate_jets():
    while True:
        for i in range(0, len(jets)):
            yield jets[i]


jet_iter = generate_jets()
shape_iter = generate_shapes()


def play_loops(n_loops):
    global tower_h
    for loop in range(0, n_loops):
        rock = next(shape_iter)
        rock.pos = (2, tower_h + drop_h)
        while True:
            # print(loop, rock.kind, rock.pos, tower_h)
            jet = next(jet_iter)
            if jet == "<":
                if rock.can_go_left():
                    # print("left")
                    rock.go_left()
            else:
                if rock.can_go_right():
                    # print("right")
                    rock.go_right()
            if rock.can_go_down():
                # print("down")
                rock.go_down()
            else:
                # print("stop")
                rock.come_to_rest()
                tower_h = max(tower_h, rock.pos[1] + rock.h)
                break


# assume memory is broken in two parts, h1 and h2
# h1 is height of lower part, h2 is height of upper part
# copy down upper part on top of lower part, and make sure memory above it is cleared
def copy_down(h1, h2):
    for i in range(0, h2):
        mem[i] = mem[h1 + i]
        mem[h1 + i] = 0
    for i in range(h2, h1):
        mem[i] = 0


# how to recognize when the tower "skyline" pattern repeats itself?
# i'm using a heuristic that works with my input (might work with yours too)
# starting with an empty chamber, run cycles and see how much tower grows each cycle
# after doing two cycles, discard the bottom of the tower from the first cycle
# continue doing cycles, discarding the bottom each time, to make a series of tower height values
# these numbers are how much the tower grows in each cycle
# the heuristic is that if we can find a pattern in these numbers, it's the answer
# to find the pattern i'm using a set to find when new, unique values appear in the series
# the code below prints out a line whenever it finds a new value in the series
# it's possible some of these numbers may be duplicated in the overall pattern,
# but let's assume there are some that only occur once in the pattern.
# if we can find such a number, then it's easy to measure the length of the pattern
# by seeing how often that number repeats.
# i make another assumption, which is that the max value in the series is such a number.
# so the code below does cycles, measures how much tower growth occurs each time,
# finds the max of this series of numbers, and counts how many cycles it takes for
# this number to occur again.  this gives the grand cycle length.
# for my input it's 344 cycles.

play_loops(n_cycle)
n_cycles = 1
h_set = set([tower_h])
max_tower_h = tower_h
n_repeats = 0
delta = 0
print(f"{n_cycles} (+{delta}), {max_tower_h}")
last_print_n_cycles = n_cycles
gc_total_h = 0
gc_start_cycle = 0

while True:
    tower_h1 = tower_h
    play_loops(n_cycle)
    n_cycles += 1
    tower_h2 = tower_h - tower_h1
    gc_total_h += tower_h2
    # found new unique h, or max has repeated again?
    if tower_h2 not in h_set or tower_h2 == max_tower_h:
        delta = n_cycles - last_print_n_cycles
        print(f"{n_cycles} (+{delta}), {tower_h2}")
        last_print_n_cycles = n_cycles
        h_set.add(tower_h2)
        if tower_h2 == max_tower_h:
            # it was a repetition of the max
            # when the grand cycle starts repeating, we won't see any more new unique values,
            # and the max will just keep printing over and over
            # let this happen a few times just to prove the pattern is really consistent, then break loop
            n_repeats += 1
            if n_repeats == 3:
                break
            # reset grand cycle height
            gc_total_h = 0
            gc_start_cycle = n_cycles
        else:
            # it was a new unique h
            max_tower_h = max(max_tower_h, tower_h2)
            n_repeats = 0

    # copy down tower 2 over tower 1
    copy_down(tower_h1, tower_h2)
    tower_h = tower_h2

print("grand cycle length is", delta, "cycles, height is", gc_total_h)
n_grand_cycle_cycles = delta
n_grand_cycle_loops = delta * n_cycle

# we kept track above of cycle that marks our GC starting point,
# but not necessarily the first such point (remember the loop above goes around some extra times)
# remove the extra GCs from our starting pont
gc_start_cycle %= n_grand_cycle_cycles

# lovely that python supports large integer math!
trillion = 1000000000000

# deduct preamble, the initial cycles before the round that marks our GC starting point
n_preamble_cycles = gc_start_cycle
print("preamble is", n_preamble_cycles, "cycles")
how_many_to_do = trillion - (n_preamble_cycles * n_cycle)

# divide out the grand cycles
ngc, remainder = divmod(how_many_to_do, n_grand_cycle_loops)
print("remainder is", remainder, "loops")

# start over, do preamble then remainder
for i in range(0, len(mem)):
    mem[i] = 0
tower_h = 0
jet_iter = generate_jets()
shape_iter = generate_shapes()

if n_preamble_cycles > 0:
    n_loops = n_cycle
    n_preamble_cycles -= 1
else:
    n_loops = min(remainder, n_cycle)
    remainder -= n_loops

play_loops(n_loops)
extra_h = tower_h

while n_preamble_cycles > 0 or remainder > 0:
    print(n_preamble_cycles, remainder, extra_h)
    if n_preamble_cycles > 0:
        n_loops = n_cycle
        n_preamble_cycles -= 1
    else:
        n_loops = min(remainder, n_cycle)
        remainder -= n_loops
    tower_h1 = tower_h
    play_loops(n_loops)
    tower_h2 = tower_h - tower_h1
    extra_h += tower_h2

    copy_down(tower_h1, tower_h2)
    tower_h = tower_h2

print("extra height is", extra_h)
print((ngc * gc_total_h) + extra_h)
