with open('input.txt') as f:
    lines = f.readlines()

grid = [[{"height": int(h), "found": False} for h in list(line.strip())] for line in lines]
nrows = len(grid)
ncols = len(grid[0])
print(f"{nrows} rows, {ncols} columns")


def generate_indices(i, j, iend, jend, istep, jstep):
    while i != iend and j != jend:
        yield i, j
        i += istep
        j += jstep


def scan(istart, jstart, iend, jend, istepouter, jstepouter, istepinner, jstepinner):
    print("scanning")
    nfound = 0
    for istartinner, jstartinner in generate_indices(istart, jstart, iend, jend, istepouter, jstepouter):
        print("start", istartinner, jstartinner)
        hmax = -1
        for i, j in generate_indices(istartinner, jstartinner, iend, jend, istepinner, jstepinner):
            print(i, j)
            if grid[i][j]["height"] > hmax:
                if not grid[i][j]["found"]:
                    grid[i][j]["found"] = True
                    nfound += 1
                hmax = grid[i][j]["height"]
                #if hmax == 9:
                    #break
    return nfound

ntotal = 0
# process rows left to right
ntotal += scan(0, 0, nrows, ncols, 1, 0, 0, 1)
# process rows right to left
ntotal += scan(0, ncols-1, nrows, -1, 1, 0, 0, -1)
# process columns top to bottom
ntotal += scan(0, 0, nrows, ncols, 0, 1, 1, 0)
# process columns bottom to top
ntotal += scan(nrows-1, 0, -1, ncols, 0, 1, -1, 0)

print(ntotal)


