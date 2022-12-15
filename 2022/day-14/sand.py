x_dim = 1024
y_dim = 256
mem = bytearray((x_dim * y_dim) // 8)


def get_bit(x, y):
    i = x + (y * x_dim)
    bit = 1 << (i % 8)
    return mem[i // 8] & bit


def set_bit(x, y, val=1):
    i = x + (y * x_dim)
    bit = 1 << (i % 8)
    if val:
        mem[i // 8] |= bit
    else:
        mem[i // 8] &= ~bit


def in_range(pt):
    return 0 <= pt[0] < x_dim and 0 <= pt[1] < y_dim


def down(pt):
    return pt[0], pt[1] + 1


def left(pt):
    return pt[0] - 1, pt[1]


def right(pt):
    return pt[0] + 1, pt[1]


def occupied(pt):
    return get_bit(pt[0], pt[1])


def set_occupied(pt):
    set_bit(pt[0], pt[1])


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


def draw_line(start_pt, end_pt):
    # print("drawing line from", start_pt, "to", end_pt)
    if start_pt == end_pt:
        # one point
        set_bit(start_pt[0], start_pt[1])
    elif start_pt[1] == end_pt[1]:
        # horizontal
        step = sign(end_pt[0] - start_pt[0])
        for x in range(start_pt[0], end_pt[0] + step, step):
            set_bit(x, start_pt[1])
    else:
        # vertical
        step = sign(end_pt[1] - start_pt[1])
        for y in range(start_pt[1], end_pt[1] + step, step):
            set_bit(start_pt[0], y)


# Dribble one unit of sand
# Return true if sand comes to rest before falling out the bottom
def dribble():
    pt = (500, 0)
    while in_range(pt):
        below = down(pt)
        if not in_range(below) or not occupied(below):
            # move down or fall out the bottom
            pt = down(pt)
        else:
            below_left = left(below)
            if not in_range(below_left):
                raise IndexError("x_dim is too small")
            if not occupied(below_left):
                pt = below_left
            else:
                below_right = right(below)
                if not in_range(below_right):
                    raise IndexError("x_dim is too small")
                if not occupied(below_right):
                    pt = below_right
                else:
                    # come to rest
                    set_occupied(pt)
                    return True
    return False


def print_section(upper_left, lower_right):
    print("".join(["V" if x == 500 else " " for x in range(upper_left[0], lower_right[0] + 1)]))
    for y in range(upper_left[1], lower_right[1] + 1):
        print("".join(["#" if occupied((x, y)) else '.' for x in range(upper_left[0], lower_right[0] + 1)]))
    print()


x_min = 99999
x_max = 0
y_max = 0


def print_board():
    print_section((x_min, 0), (x_max, y_max))


with open('input.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        points = [[int(val) for val in vals.split(",")] for vals in line.split(" -> ")]
        for i in range(0, len(points) - 1):
            draw_line(points[i], points[i + 1])
            x_min = min(x_min, points[i + 1][0])
            x_max = max(x_max, points[i + 1][0])
            y_max = max(y_max, points[i + 1][1])

    print("x_min", x_min)
    print("x_max", x_max)
    print("y_max", y_max)
    print_board()

    # comment these lines for part 1, uncomment for part 2
    # draw floor line for part 2
    y_max += 2
    draw_line((0, y_max), (x_dim - 1, y_max))

    n = 0
    while dribble():
        n += 1
        if occupied((500, 0)):
            break

    print_section((400, 0), (600, y_max))
    print(n)
