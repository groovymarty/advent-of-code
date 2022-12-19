n_loops = 2022
max_shape_h = 4
drop_h = 3
chamber_w = 7
y_dim = (n_loops * max_shape_h) + drop_h + max_shape_h
x_dim = 8
mem = bytearray((x_dim * y_dim) // 8)
tower_h = 0
skyline = [0 for i in range(0, chamber_w)]


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


def normalize_skyline():
    global skyline
    c = min(val for val in skyline)
    skyline = [val - c for val in skyline]


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
        skyline[x] += 1
        skyline[x + 1] += 1
        skyline[x + 2] += 1
        skyline[x + 3] += 1
        normalize_skyline()


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
        skyline[x] += 2
        skyline[x + 1] += 3
        skyline[x + 2] += 2
        normalize_skyline()


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
        skyline[x] += 1
        skyline[x + 1] += 1
        skyline[x + 2] += 3
        normalize_skyline()


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
        skyline[x] += 4
        normalize_skyline()


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
        skyline[x] += 2
        skyline[x + 1] += 2
        normalize_skyline()


def generate_shapes():
    while True:
        yield ShapeHLine()
        yield ShapePlus()
        yield ShapeLRCorner()
        yield ShapeVLine()
        yield ShapeBox()



with open('input.txt') as f:
    jets = f.readlines()[0].strip()


def generate_jets():
    while True:
        for i in range(0, len(jets)):
            yield jets[i]


jet_iter = generate_jets()
shape_iter = generate_shapes()

for loop in range(0, n_loops):
    rock = next(shape_iter)
    rock.pos = (2, tower_h + drop_h)
    while True:
        print(loop, rock.kind, rock.pos, tower_h)
        jet = next(jet_iter)
        if jet == "<":
            if rock.can_go_left():
                print("left")
                rock.go_left()
        else:
            if rock.can_go_right():
                print("right")
                rock.go_right()
        if rock.can_go_down():
            print("down")
            rock.go_down()
        else:
            print("stop")
            rock.come_to_rest()
            tower_h = max(tower_h, rock.pos[1] + rock.h)
            break

print(tower_h)
print(skyline)
