with open('input.txt') as f:
    lines = f.readlines()

# grid is array of arrays
# each element in grid is a small object (a dictionary) with two elements:
# height is the integer height of the tree, 1-9
# found is a boolean that's set true when this tree is counted as visible
grid = [[{"height": int(h), "found": False} for h in list(line.strip())] for line in lines]
nrows = len(grid)
ncols = len(grid[0])
print(f"{nrows} rows, {ncols} columns")


# generator to make a series of (row,col) index pairs
# start, end, step are two-element tuples specifying the parameters for each axis
# as used in this application one axis remains constant and the other iterates from start to end
# however the generator could be used to advance both axes simultaneously
# the generator stops when one or the other index reaches the end of its range
def generate_indices(start, end, step):
    i, j = start
    while i != end[0] and j != end[1]:
        yield i, j
        i += step[0]
        j += step[1]


# scan across the grid according to parameters
def scan(start, end, stepouter, stepinner):
    print("scanning")
    nfound = 0
    # here is the outer loop which generates the starting coordinates for the inner loop
    for startinner in generate_indices(start, end, stepouter):
        print("start", startinner)
        # this variable keeps track of the highest tree seen in this pass
        # initializing to -1 forces first tree always to be visible
        hmax = -1
        # here is the inner loop
        for i, j in generate_indices(startinner, end, stepinner):
            print(i, j)
            # is this tree higher than the highest one seen so far?
            if grid[i][j]["height"] > hmax:
                # count it, unless it's already been counted
                if not grid[i][j]["found"]:
                    grid[i][j]["found"] = True
                    nfound += 1
                # we have a new highest one
                hmax = grid[i][j]["height"]
                # optimization, early exit if no higher trees are possible
                if hmax == 9:
                    break
    return nfound

ntotal = 0
# process rows left to right
ntotal += scan((0, 0), (nrows, ncols), (1, 0), (0, 1))
# process rows right to left
ntotal += scan((0, ncols-1), (nrows, -1), (1, 0), (0, -1))
# process columns top to bottom
ntotal += scan((0, 0), (nrows, ncols), (0, 1), (1, 0))
# process columns bottom to top
ntotal += scan((nrows-1, 0), (-1, ncols), (0, 1), (-1, 0))

print(ntotal)


