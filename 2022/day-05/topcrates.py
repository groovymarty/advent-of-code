import re

stacks = []
with open('input.txt') as f:
    lines = f.readlines()
    # remove newline at end of each line
    lines = [line.strip() for line in lines]
    # find blank line
    iblank = lines.index("")
    # split input into header and moves
    # ignore row of numbers at bottom of header
    header = lines[0:iblank-1]
    moves = lines[iblank+1:]
    # process header lines in reverse order
    header.reverse()
    # initialize stacks
    for line in header:
        # number of columns in this line
        ncols = (len(line) + 1) // 4
        # make more stacks as needed, should only happen in first loop
        while len(stacks) < ncols:
            stacks.append([])
        # push letters onto stacks
        for i in range(0, ncols):
            letter = line[(i * 4) + 1]
            if letter != " ":
                stacks[i].append(letter)
    # process moves
    for line in moves:
        mr = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        if not mr:
            print(f"error, invalid line: {line}")
            break
        move_n = int(mr.group(1))
        move_from = int(mr.group(2))
        move_to = int(mr.group(3))
        for n in range(0, move_n):
            if len(stacks[move_from-1]) == 0:
                print(f"error, stack {move_from} is empty for move: {line}")
                break
            letter = stacks[move_from-1].pop()
            stacks[move_to-1].append(letter)

# print letter at top of each stack
tops = [stack.pop() if len(stack) > 0 else " " for stack in stacks]
print("".join(tops))
