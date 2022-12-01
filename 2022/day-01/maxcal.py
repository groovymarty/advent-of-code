maxcal = 0
curcal = 0
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            curcal += int(line)
        else:
            if curcal > maxcal:
                maxcal = curcal
            curcal = 0
print(maxcal)
