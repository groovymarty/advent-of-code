with open('input.txt') as f:
    lines = f.readlines()
    points = [tuple(int(val) for val in line.strip().split(",")) for line in lines]

min_pt = tuple(min(pt[i] for pt in points) for i in range(0, 3))
max_pt = tuple(max(pt[i] for pt in points) for i in range(0, 3))
print(min_pt, max_pt)

# assume min_pt is (0, 0, 0), no harm besides wasting memory if this is not true
max_x, max_y, max_z = max_pt

# add extra to make a 2-wide border around the edges so we don't have to worry about indexing off the edges
dim_x, dim_y, dim_z = tuple(max_val + 5 for max_val in max_pt)

# two bits per point
n_per_pt = 2
OCCUPIED = 0
EXTERIOR = 1

mem = bytearray((n_per_pt * dim_x * dim_y * dim_z + 7) // 8)

# offset added below so we can tolerate index values (x, y or z) out of range by 2
bit_index_offset = (((2 * dim_y + 2) * dim_x) + 2) * n_per_pt


def get_bit(which_bit, x, y, z):
    i = (((((z * dim_y) + y) * dim_x) + x) * n_per_pt) + which_bit + bit_index_offset
    bit = 1 << (i % 8)
    return mem[i // 8] & bit


def set_bit(which_bit, x, y, z, val=1):
    i = (((((z * dim_y) + y) * dim_x) + x) * n_per_pt) + which_bit + bit_index_offset
    bit = 1 << (i % 8)
    if val:
        mem[i // 8] |= bit
    else:
        mem[i // 8] &= ~bit


def print_mem():
    for z in range(-1, max_z + 2):
        print("z = ", z)
        for y in range(-1, max_y + 2):
            print("".join(["#" if get_bit(OCCUPIED, x, y, z) else "." if get_bit(EXTERIOR, x, y, z) else " " for x in range(-1, max_x + 2)]))


# set bits for all cubes
for pt in points:
    set_bit(OCCUPIED, pt[0], pt[1], pt[2])

# for each cube, count number of exposed sides
n_exposed_sides = 0
for pt in points:
    x, y, z = pt
    # top
    if not get_bit(OCCUPIED, x, y, z+1):
        n_exposed_sides += 1
    # bottom
    if not get_bit(OCCUPIED, x, y, z-1):
        n_exposed_sides += 1
    # back
    if not get_bit(OCCUPIED, x, y+1, z):
        n_exposed_sides += 1
    # front
    if not get_bit(OCCUPIED, x, y-1, z):
        n_exposed_sides += 1
    # left
    if not get_bit(OCCUPIED, x-1, y, z):
        n_exposed_sides += 1
    # right
    if not get_bit(OCCUPIED, x+1, y, z):
        n_exposed_sides += 1

print(n_exposed_sides)


# find an exterior starting point
def find_start_pt():
    for x in range(0, max_x + 1):
        for y in range(0, max_y + 1):
            for z in range(0, max_z + 1):
                if not get_bit(OCCUPIED, x, y, z):
                    return x, y, z
    return None


start_pt = find_start_pt()
if start_pt is None:
    raise ValueError("No starting point")

print("starting point", start_pt)

# set EXTERIOR bits to block pouring at edges
# there's still a 1-wide margin around the lava droplet to allow the paint pouring algorithm to
# wrap completely around it
for x in range(-2, max_x + 2):
    for y in range(-2, max_y + 2):
        set_bit(EXTERIOR, x, y, -2)
        set_bit(EXTERIOR, x, y, max_z + 2)
    for z in range(-2, max_z + 2):
        set_bit(EXTERIOR, x, -2, z);
        set_bit(EXTERIOR, x, max_y + 2, z)
for y in range(-2, max_y + 2):
    for z in range(-2, max_z + 2):
        set_bit(EXTERIOR, -2, y, z);
        set_bit(EXTERIOR, max_x + 2, y, z)

# print_mem()

# directions
UP = 0
DOWN = 1
BACK = 2
FRONT = 3
RIGHT = 4
LEFT = 5
N_DIR = 6

# movements
move_x = (0, 0, 0, 0, 1, -1)
move_y = (0, 0, 1, -1, 0, 0)
move_z = (1, -1, 0, 0, 0, 0)

# pour paint into exterior space
stack = []
pt = start_pt
next_dir = UP
while True:
    x, y, z = pt
    set_bit(EXTERIOR, x, y, z)
    # try next direction
    if next_dir < N_DIR:
        next_x = x + move_x[next_dir]
        next_y = y + move_y[next_dir]
        next_z = z + move_z[next_dir]
        if not get_bit(OCCUPIED, next_x, next_y, next_z) and not get_bit(EXTERIOR, next_x, next_y, next_z):
            # not occupied and not already poured, explore this point
            stack.append((pt, next_dir + 1))
            pt = (next_x, next_y, next_z)
            next_dir = UP
        else:
            next_dir += 1
    elif len(stack) > 1:
        pt, next_dir = stack.pop()
    else:
        break

print_mem()

# count exterior sides
n_exterior_sides = 0
for pt in points:
    x, y, z = pt
    # top
    if not get_bit(OCCUPIED, x, y, z+1) and get_bit(EXTERIOR, x, y, z+1):
        n_exterior_sides += 1
    # bottom
    if not get_bit(OCCUPIED, x, y, z-1) and get_bit(EXTERIOR, x, y, z-1):
        n_exterior_sides += 1
    # back
    if not get_bit(OCCUPIED, x, y+1, z) and get_bit(EXTERIOR, x, y+1, z):
        n_exterior_sides += 1
    # front
    if not get_bit(OCCUPIED, x, y-1, z) and get_bit(EXTERIOR, x, y-1, z):
        n_exterior_sides += 1
    # left
    if not get_bit(OCCUPIED, x-1, y, z) and get_bit(EXTERIOR, x-1, y, z):
        n_exterior_sides += 1
    # right
    if not get_bit(OCCUPIED, x+1, y, z) and get_bit(EXTERIOR, x+1, y, z):
        n_exterior_sides += 1

print(n_exterior_sides)
