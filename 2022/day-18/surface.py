with open('input.txt') as f:
    lines = f.readlines()
    points = [tuple(int(val) for val in line.strip().split(",")) for line in lines]

min_pt = tuple(min(pt[i] for pt in points) for i in range(0, 3))
max_pt = tuple(max(pt[i] for pt in points) for i in range(0, 3))
print(min_pt, max_pt)

# assume min_pt is (0, 0, 0), no harm besides wasting memory if this is not true

# add 2 to make a 1-wide border around the edges so we don't to worry about indexing off the edges
dim_x, dim_y, dim_z = tuple(max_val + 3 for max_val in max_pt)
mem = bytearray((dim_x * dim_y * dim_z + 7) // 8)

# offset added below so we can tolerate index values (x, y or z) out of range by 1
bit_index_offset = ((dim_y + 1) * dim_x) + 1


def get_bit(x, y, z):
    i = (((z * dim_y) + y) * dim_x) + x + bit_index_offset
    bit = 1 << (i % 8)
    return mem[i // 8] & bit


def set_bit(x, y, z, val=1):
    i = (((z * dim_y) + y) * dim_x) + x + bit_index_offset
    bit = 1 << (i % 8)
    if val:
        mem[i // 8] |= bit
    else:
        mem[i // 8] &= ~bit


# set bits for all cubes
for pt in points:
    set_bit(pt[0], pt[1], pt[2])

# for each cube, count number of exposed sides
n_exposed_sides = 0
for pt in points:
    x, y, z = pt
    # top
    if not get_bit(x, y, z+1):
        n_exposed_sides += 1
    # bottom
    if not get_bit(x, y, z-1):
        n_exposed_sides += 1
    # back
    if not get_bit(x, y+1, z):
        n_exposed_sides += 1
    # front
    if not get_bit(x, y-1, z):
        n_exposed_sides += 1
    # left
    if not get_bit(x-1, y, z):
        n_exposed_sides += 1
    # right
    if not get_bit(x+1, y, z):
        n_exposed_sides += 1

print(n_exposed_sides)
