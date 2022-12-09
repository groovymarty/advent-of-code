from collections import Counter

visited = Counter()
knots = [(0, 0) for i in range(0, 10)]
visited[(0, 0)] = 1


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
            head = knots[0]
            if direction == "U":
                head = (head[0] - 1, head[1])
            elif direction == "D":
                head = (head[0] + 1, head[1])
            elif direction == "L":
                head = (head[0], head[1] - 1)
            elif direction == "R":
                head = (head[0], head[1] + 1)
            knots[0] = head
            # print_board()
            # print("-----------")

            # now move remaining knots as required by rules
            for i in range(1, 10):
                knot = knots[i]
                prev = knots[i-1]
                if prev[0] == knot[0]:
                    # same row
                    dist = knot[1] - prev[1]
                    if abs(dist) > 1:
                        # too far apart, move tail closer on same row
                        knot = (knot[0], knot[1] - sign(dist))
                elif prev[1] == knot[1]:
                    # same col
                    dist = knot[0] - prev[0]
                    if abs(dist) > 1:
                        # too far apart, move tail closer on same col
                        knot = (knot[0] - sign(dist), knot[1])
                else:
                    # different row and col
                    rowdist = knot[0] - prev[0]
                    coldist = knot[1] - prev[1]
                    if abs(rowdist) > 1 or abs(coldist) > 1:
                        # too far apart, move diagonally
                        knot = (knot[0] - sign(rowdist), knot[1] - sign(coldist))
                knots[i] = knot
            # print_board()
            # print("===========")

            # keep track of tail positions visited
            tail = knots[9]
            visited[tail] = 1

print(len(visited))
