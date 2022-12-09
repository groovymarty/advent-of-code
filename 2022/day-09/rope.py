from collections import Counter

visited = Counter()
head = (0, 0)
tail = (0, 0)
visited[tail] = 1

# for print_board
minrow = -1
maxrow = 1
mincol = -1
maxcol = 1


def print_board():
    global minrow, maxrow, mincol, maxcol
    minrow = min(minrow, head[0], tail[0])
    maxrow = max(maxrow, head[0], tail[0])
    mincol = min(mincol, head[1], tail[1])
    maxcol = max(maxcol, head[1], tail[1])
    for row in range(minrow, maxrow+1):
        line = ""
        for col in range(mincol, maxcol+1):
            pos = (row, col)
            line += "H " if pos == head else "T " if pos == tail else ". "
        print(line)


def sign(val):
    return 1 if val > 0 else -1 if val < 0 else 0


# print_board()
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        # print(f"=== {line} ===")
        direction = line[0]
        amount = int(line[2:])
        for n in range(0, amount):
            # move head
            if direction == "U":
                head = (head[0] - 1, head[1])
            elif direction == "D":
                head = (head[0] + 1, head[1])
            elif direction == "L":
                head = (head[0], head[1] - 1)
            elif direction == "R":
                head = (head[0], head[1] + 1)
            # print_board()
            # print("-----------")

            # now move tail as required by rules
            if head[0] == tail[0]:
                # same row
                dist = tail[1] - head[1]
                if abs(dist) > 1:
                    # too far apart, move tail closer on same row
                    tail = (tail[0], tail[1] - sign(dist))
            elif head[1] == tail[1]:
                # same col
                dist = tail[0] - head[0]
                if abs(dist) > 1:
                    # too far apart, move tail closer on same col
                    tail = (tail[0] - sign(dist), tail[1])
            else:
                # different row and col
                rowdist = tail[0] - head[0]
                coldist = tail[1] - head[1]
                if abs(rowdist) > 1 or abs(coldist) > 1:
                    # too far apart, move diagonally
                    tail = (tail[0] - sign(rowdist), tail[1] - sign(coldist))
            # print_board()
            # print("===========")

            # keep track of tail positions visited
            visited[tail] = 1

print(len(visited))
