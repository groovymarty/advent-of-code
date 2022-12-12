with open('input.txt') as f:
    lines = f.readlines()

# grid is array of arrays
# value of each element is letter but we'll remap below to elevation as integer 0-25
grid = [[x for x in list(line.strip())] for line in lines]
nrows = len(grid)
ncols = len(grid[0])
print(f"{nrows} rows, {ncols} columns")

# positions visited and length of shortest path found to get there
visited = [[None for j in range(0, ncols)] for i in range(0, nrows)]

start = None
goal = None

# find starting/ending position
# remap grid from letters to numerical elevation (0 to 25)
for i in range(0, nrows):
    for j in range(0, ncols):
        if grid[i][j] == "S":
            start = (i, j)
            grid[i][j] = 0
        elif grid[i][j] == "E":
            goal = (i, j)
            grid[i][j] = 25
        elif ord("a") <= ord(grid[i][j]) <= ord("z"):
            grid[i][j] = ord(grid[i][j]) - ord("a")
        else:
            raise ValueError(f"Bad character {grid[i][j]} at grid[{i}, {j}]")

if start is None:
    raise ValueError("Start position not found")
if goal is None:
    raise ValueError("End position not found")
print("start is", start)
print("end is", goal)

# directions to try at each position
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

# direction names
dir_names = ["RIGHT", "DOWN", "LEFT", "UP"]


# advance in specified direction
def advance(pos, dir):
    return pos[0] + [0, 1, 0, -1][dir], pos[1] + [1, 0, -1, 0][dir]


# return true if move is valid
def is_valid_move(old_pos, new_pos):
    return \
        0 <= new_pos[0] < nrows and \
        0 <= new_pos[1] < ncols and \
        grid[old_pos[0]][old_pos[1]] + 1 >= grid[new_pos[0]][new_pos[1]]


# current position
pos = start
visited[start[0]][start[1]] = 0

# next direction to consider at current position (in order per above enum)
dir = RIGHT

# each stack element is two-element tuple of (pos, dir) values
stack = []

# shortest path length to goal
shortest = None

while True:
    if dir <= UP:
        next_pos = advance(pos, dir)
        dir += 1
        if is_valid_move(pos, next_pos):
            # print("is valid move")
            if next_pos == goal:
                print(f"found goal! path length is {len(stack) + 1}")
                if shortest is None:
                    shortest = len(stack) + 1
                else:
                    shortest = min(shortest, len(stack) + 1)
            elif visited[next_pos[0]][next_pos[1]] is None or \
                visited[next_pos[0]][next_pos[1]] > len(stack) + 1:
                # haven't visited this location before, or just found a better way to get here
                # print(f"pushing stack to visit {next_pos[0]}, {next_pos[1]}")
                stack.append((pos, dir))
                pos = next_pos
                dir = RIGHT
                visited[pos[0]][pos[1]] = len(stack)
        else:
            # print("not valid move")
            pass
    elif len(stack) > 0:
        # print("popping stack")
        pos, dir = stack.pop()
    else:
        # print("done")
        break

print(shortest)
