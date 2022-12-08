with open('input.txt') as f:
    lines = f.readlines()

# grid is array of arrays
# each element in grid is a small object (a dictionary) with one element:
# height is the integer height of the tree, 1-9
grid = [[{"height": int(h)} for h in list(line.strip())] for line in lines]
nrows = len(grid)
ncols = len(grid[0])
print(f"{nrows} rows, {ncols} columns")


# generator to make a series of (row,col) index pairs
# start, end, step are two-element tuples specifying the parameters for each axis
# as used in this application one axis remains constant and the other iterates from start to end
# however the generator could be used to advance both axes simultaneously
# unlike the previous generator, this one stops when both indices reaches the end of their range
def generate_indices(start, end, step):
    i, j = start
    while i != end[0] or j != end[1]:
        yield i, j
        i += step[0]
        j += step[1]


# return number of trees visible from starting tree in a given direction
def scan(start, end, step):
    # count number of trees visible from starting point
    nview = 0
    # create generator according to parameters
    gen = generate_indices(start, end, step)
    # get the starting point and height of tree there
    i, j = next(gen)
    print("scanning from", i, j)
    h = grid[i][j]["height"]
    # continue generating index pairs in specified direction until hit edge
    for i, j in gen:
        print(i, j)
        # always count the next tree but stop if height criterion met
        nview += 1
        if grid[i][j]["height"] >= h:
            break
    return nview

maxscore = 0

# consider all trees
for i in range(0, nrows):
    for j in range(0, ncols):
        # scan in all four directions from this tree
        score = 1
        # scan right
        score *= scan((i, j), (i, ncols), (0, 1))
        # scan left
        score *= scan((i, j), (i, -1), (0, -1))
        # scan down
        score *= scan((i, j), (nrows, j), (1, 0))
        # scan up
        score *= scan((i, j), (-1, j), (-1, 0))
        # update max
        if score > maxscore:
            maxscore = score

print(maxscore)
